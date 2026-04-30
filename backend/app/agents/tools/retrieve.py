import logging
from typing import List

from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)


async def retrieve_context(
    query: str,
    rag_service: RAGService,
    top_k: int = 5,
) -> List[dict]:
    """Retrieve relevant chunks from Pinecone for a given query."""
    logger.info(f"Tool: retrieve_context | query='{query[:60]}' top_k={top_k}")
    return await rag_service.retrieve(query, top_k=top_k)
