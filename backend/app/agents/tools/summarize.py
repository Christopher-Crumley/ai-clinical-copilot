import json
import logging

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


async def summarize_note(context: str, client: AsyncOpenAI, model: str) -> str:
    """Generate a concise clinical summary from retrieved context."""
    logger.info(f"Tool: summarize_note | context length={len(context)}")
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a clinical documentation assistant. "
                    "Produce a concise 2-3 sentence summary of the clinical note. "
                    "Focus on the chief complaint, key findings, and plan."
                ),
            },
            {"role": "user", "content": f"Clinical note:\n{context}"},
        ],
    )
    return response.choices[0].message.content


async def generate_soap(context: str, client: AsyncOpenAI, model: str) -> dict:
    """Extract SOAP components from clinical context using structured JSON output."""
    logger.info(f"Tool: generate_soap | context length={len(context)}")
    response = await client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a clinical documentation assistant. "
                    "Extract SOAP note components from the provided clinical text. "
                    "Return a JSON object with exactly these keys: "
                    "subjective, objective, assessment, plan. "
                    "Each value should be a clear, concise string."
                ),
            },
            {"role": "user", "content": f"Clinical note:\n{context}"},
        ],
    )
    return json.loads(response.choices[0].message.content)
