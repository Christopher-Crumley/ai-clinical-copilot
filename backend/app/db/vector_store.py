import asyncio
import logging
from typing import List

from pinecone import Pinecone

from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Pinecone wrapper for upsert and similarity search."""

    def __init__(self):
        pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = pc.Index(settings.pinecone_index_name)

    async def upsert(self, vectors: List[dict]) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: self.index.upsert(vectors=vectors))
        logger.info(f"VectorStore.upsert | {len(vectors)} vectors")

    async def query(self, embedding: List[float], top_k: int = 5) -> List[dict]:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.index.query(vector=embedding, top_k=top_k, include_metadata=True),
        )
        return [
            {"id": m.id, "score": m.score, "metadata": m.metadata}
            for m in response.matches
        ]
