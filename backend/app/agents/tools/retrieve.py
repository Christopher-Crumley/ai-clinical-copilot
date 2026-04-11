import logging
from typing import List

logger = logging.getLogger(__name__)


async def retrieve_context(query: str, top_k: int = 5) -> List[dict]:
    """
    Tool: retrieve relevant chunks from Pinecone for a given query.

    Phase 3: wire to RAGService.retrieve()
    Returns list of {content, score, metadata}
    """
    logger.info(f"Tool: retrieve_context | query='{query[:60]}' top_k={top_k}")
    return []
