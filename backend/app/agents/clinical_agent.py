import logging
from typing import AsyncIterator, Optional

from openai import AsyncOpenAI

from app.agents.tools.retrieve import retrieve_context
from app.agents.tools.summarize import generate_soap, summarize_note
from app.core.config import settings
from app.services.rag_service import RAGService
from app.utils.formatting import format_soap_note

logger = logging.getLogger(__name__)

_chat_history: dict[str, list[dict]] = {}
_MAX_HISTORY = 10


def _detect_intent(message: str) -> str:
    lower = message.lower()
    if any(w in lower for w in ["soap", "subjective", "objective", "assessment"]):
        return "soap"
    if any(w in lower for w in ["summarize", "summary", "summarise", "tldr"]):
        return "summarize"
    return "qa"


class ClinicalAgent:
    """
    Core reasoning agent: detects intent, retrieves context, dispatches to tools,
    and maintains per-session chat history.
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.rag_service = RAGService()
        self.model = settings.model_name

    async def run(self, message: str, session_id: Optional[str] = None) -> dict:
        logger.info(f"ClinicalAgent.run | '{message[:60]}'")

        history = list(_chat_history.get(session_id, [])) if session_id else []
        intent = _detect_intent(message)
        logger.info(f"ClinicalAgent.run | intent={intent}")

        chunks = await retrieve_context(message, self.rag_service, top_k=settings.top_k)
        context = "\n\n".join(c["content"] for c in chunks)

        soap_note = None
        summary = None

        if intent == "soap":
            soap_data = await generate_soap(context, self.client, self.model)
            soap_note = soap_data
            response_message = format_soap_note(
                soap_data.get("subjective", ""),
                soap_data.get("objective", ""),
                soap_data.get("assessment", ""),
                soap_data.get("plan", ""),
            )

        elif intent == "summarize":
            summary = await summarize_note(context, self.client, self.model)
            response_message = summary

        else:
            system_content = (
                "You are a clinical documentation assistant. "
                "Answer the user's question using the provided clinical context. "
                "Be concise and accurate."
            )
            if context:
                system_content += f"\n\nRelevant clinical context:\n{context}"

            messages = [{"role": "system", "content": system_content}]
            messages.extend(history[-_MAX_HISTORY:])
            messages.append({"role": "user", "content": message})

            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            response_message = resp.choices[0].message.content

        if session_id:
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response_message})
            _chat_history[session_id] = history[-_MAX_HISTORY:]

        return {
            "message": response_message,
            "sources": chunks,
            "session_id": session_id,
            "soap_note": soap_note,
            "summary": summary,
        }

    async def stream(
        self, message: str, session_id: Optional[str] = None
    ) -> AsyncIterator[str]:
        history = list(_chat_history.get(session_id, [])) if session_id else []

        chunks = await retrieve_context(message, self.rag_service, top_k=settings.top_k)
        context = "\n\n".join(c["content"] for c in chunks)

        system_content = (
            "You are a clinical documentation assistant. "
            "Answer the user's question using the provided clinical context. "
            "Be concise and accurate."
        )
        if context:
            system_content += f"\n\nRelevant clinical context:\n{context}"

        messages = [{"role": "system", "content": system_content}]
        messages.extend(history[-_MAX_HISTORY:])
        messages.append({"role": "user", "content": message})

        tokens: list[str] = []
        async with await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        ) as stream:
            async for chunk in stream:
                token = chunk.choices[0].delta.content
                if token:
                    tokens.append(token)
                    yield token

        if session_id:
            response_text = "".join(tokens)
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response_text})
            _chat_history[session_id] = history[-_MAX_HISTORY:]
