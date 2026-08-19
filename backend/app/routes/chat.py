import logging

from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service

logger = logging.getLogger("kisanai")
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        result = chat_service.get_reply(payload.message, payload.language)
    except Exception as exc:  # noqa: BLE001
        logger.exception("chat service failed")
        raise HTTPException(status_code=502, detail="AI assistant is temporarily unavailable") from exc

    return ChatResponse(reply=result["reply"], sources=result["sources"], language=payload.language)
