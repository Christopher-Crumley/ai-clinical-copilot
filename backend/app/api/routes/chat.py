import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
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


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    logger.info(f"Stream request received | session={request.session_id}")

    async def event_stream():
        async for token in agent.stream(request.message, request.session_id):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
