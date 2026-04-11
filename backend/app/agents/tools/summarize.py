import logging

logger = logging.getLogger(__name__)


async def summarize_note(text: str) -> str:
    """
    Tool: generate a concise clinical summary from raw note text.

    Phase 3: wire to GPT-4o with a clinical summarization prompt.
    """
    logger.info(f"Tool: summarize_note | input length={len(text)}")
    return "[Summarization tool — wires in Phase 3]"


async def generate_soap(text: str) -> dict:
    """
    Tool: extract SOAP components from unstructured clinical text.

    Phase 3: prompt GPT-4o for structured JSON output with
    subjective / objective / assessment / plan fields.
    """
    logger.info(f"Tool: generate_soap | input length={len(text)}")
    return {
        "subjective": "",
        "objective": "",
        "assessment": "",
        "plan": "",
    }
