from pydantic import BaseModel


class IngestResponse(BaseModel):
    filename: str
    status: str
    chunks_stored: int
    message: str
