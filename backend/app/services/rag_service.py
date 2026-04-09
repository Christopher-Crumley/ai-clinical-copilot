import logging
from typing import List

from app.core.config import settings
from app.db.vector_store import VectorStore
from app.services.embedding_service import EmbeddingService
from app.utils.chunking import chunk_text

logger = logging.getLogger(__name__)


class RAGService:
    """Handles document ingestion and retrieval via Pinecone."""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    async def ingest(self, text: str, filename: str) -> int:
        logger.info(f"RAGService.ingest | filename={filename}")
        chunks = chunk_text(text, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap)
        embeddings = await self.embedding_service.embed_batch(chunks)
        vectors = [
            {
                "id": f"{filename}_{i}",
                "values": embeddings[i],
                "metadata": {"text": chunks[i], "filename": filename},
            }
            for i in range(len(chunks))
        ]
        await self.vector_store.upsert(vectors)
        logger.info(f"RAGService.ingest | stored {len(chunks)} chunks")
        return len(chunks)

    async def retrieve(self, query: str, top_k: int = 5) -> List[dict]:
        logger.info(f"RAGService.retrieve | query='{query[:60]}' top_k={top_k}")
        embedding = await self.embedding_service.embed(query)
        matches = await self.vector_store.query(embedding, top_k=top_k)
        return [
            {
                "content": m["metadata"].get("text", ""),
                "score": m["score"],
                "metadata": m["metadata"],
            }
            for m in matches
        ]
