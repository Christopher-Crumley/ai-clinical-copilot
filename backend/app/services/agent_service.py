import logging
from typing import Optional

from openai import AsyncOpenAI

from app.core.config import settings
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)


class AgentService:
    """Orchestrates RAG retrieval and LLM response generation."""

    def __init__(self):
        self.rag_service = RAGService()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def run(self, message: str, session_id: Optional[str] = None) -> dict:
        logger.info(f"AgentService.run | message='{message[:60]}'")

        results = await self.rag_service.retrieve(message, top_k=settings.top_k)

        if not results:
            return {
                "message": "No relevant documents were found to answer your question.",
                "sources": [],
                "session_id": session_id,
            }

        context_block = "\n\n".join(
            f"[{i + 1}] {r['content']}" for i, r in enumerate(results)
        )

        response = await self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a clinical documentation assistant. "
                        "Answer questions only based on the provided clinical context. "
                        "If the context does not contain the answer, say so clearly."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_block}\n\nQuestion: {message}",
                },
            ],
        )

        return {
            "message": response.choices[0].message.content,
            "sources": results,
            "session_id": session_id,
        }
