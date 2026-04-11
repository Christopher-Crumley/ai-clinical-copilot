import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ClinicalAgent:
    """
    The core reasoning agent.

    Phase 3 implementation:
      - Receives user message + session history
      - Decides which tools to call (retrieve, summarize, generate_soap)
      - Passes retrieved context to GPT-4o
      - Returns structured response
    """

    def __init__(self):
        # Phase 3: initialize OpenAI client, RAGService, tool registry
        pass

    async def run(self, message: str, session_id: Optional[str] = None) -> dict:
        logger.info(f"ClinicalAgent.run | '{message[:60]}'")
        # Phase 3 implementation
        return {
            "message": "Clinical agent stub — wires in Phase 3.",
            "sources": [],
            "session_id": session_id,
        }
