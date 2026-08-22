import logging

from fastapi import APIRouter, HTTPException

from app.schemas.schemes import SchemeQueryRequest, SchemeQueryResponse
from app.services import schemes_service

logger = logging.getLogger("kisanai")
router = APIRouter()


@router.post("/schemes/query", response_model=SchemeQueryResponse)
def query_schemes(payload: SchemeQueryRequest):
    try:
        result = schemes_service.query(payload.question, payload.language)
    except Exception as exc:  # noqa: BLE001
        logger.exception("schemes service failed")
        raise HTTPException(status_code=502, detail="Scheme assistant is temporarily unavailable") from exc

    return SchemeQueryResponse(answer=result["answer"], schemes=result["schemes"], language=payload.language)
