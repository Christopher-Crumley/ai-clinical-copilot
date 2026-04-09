import io
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile
from pypdf import PdfReader

from app.schemas.document import IngestResponse
from app.services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_TYPES = {"text/plain", "application/pdf"}


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Upload .txt or .pdf.",
        )

    contents = await file.read()
    size_kb = round(len(contents) / 1024, 1)
    logger.info(f"File received: {file.filename} ({size_kb} KB)")

    if file.content_type == "text/plain":
        text = contents.decode("utf-8")
    else:
        reader = PdfReader(io.BytesIO(contents))
        text = "".join(page.extract_text() or "" for page in reader.pages)

    rag = RAGService()
    chunks_stored = await rag.ingest(text, file.filename)

    return IngestResponse(
        filename=file.filename,
        status="ingested",
        chunks_stored=chunks_stored,
        message=f"Ingested {chunks_stored} chunks from {file.filename}.",
    )
