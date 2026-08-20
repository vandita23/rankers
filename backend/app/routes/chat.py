import logging

from fastapi import APIRouter, HTTPException
from psycopg2.extras import Json

from app.core.db import query
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service

logger = logging.getLogger("kisanai")

router = APIRouter()

DEMO_FARMER_ID = 1


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        # Generate the response using Gemini.
        result = chat_service.get_reply(
            payload.message,
            payload.language,
        )

        # Store the conversation in Supabase.
        query(
            """
            INSERT INTO chat_logs
                (farmer_id, message, language, reply, sources)
            VALUES
                (%s, %s, %s, %s, %s)
            """,
            (
                DEMO_FARMER_ID,
                payload.message,
                payload.language,
                result["reply"],
                Json(result["sources"]),
            ),
            fetch_all=False,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("chat request failed")
        raise HTTPException(
            status_code=502,
            detail="AI assistant is temporarily unavailable",
        ) from exc

    return ChatResponse(
        reply=result["reply"],
        sources=result["sources"],
        language=payload.language,
    )