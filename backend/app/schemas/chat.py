from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class Source(BaseModel):
    content: str
    score: float
    metadata: dict = {}


class SoapNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str


class ChatResponse(BaseModel):
    message: str
    sources: List[Source] = []
    session_id: Optional[str] = None
    soap_note: Optional[SoapNote] = None
    summary: Optional[str] = None
