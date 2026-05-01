import logging
from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.clinical_agent import ClinicalAgent

router = APIRouter()
logger = logging.getLogger(__name__)
agent = ClinicalAgent()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Chat request received | session={request.session_id}")
    result = await agent.run(
        message=request.message,
        session_id=request.session_id,
    )
    return ChatResponse(**result)
