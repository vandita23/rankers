import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.disease import DiseaseResponse
from app.services import disease_service

logger = logging.getLogger("kisanai")
router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB


@router.post("/disease/predict", response_model=DiseaseResponse)
async def predict_disease(image: UploadFile = File(...), language: str = Form(default="en")):
    if language not in ("en", "hi"):
        raise HTTPException(status_code=422, detail="language must be 'en' or 'hi'")

    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=422, detail=f"Unsupported image type: {image.content_type}")

    contents = await image.read()
    if not contents:
        raise HTTPException(status_code=422, detail="Uploaded image is empty")
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=422, detail="Image is too large (max 8MB)")

    try:
        result = disease_service.predict(contents, language)
    except Exception as exc:  # noqa: BLE001
        logger.exception("disease prediction failed")
        raise HTTPException(status_code=502, detail="Disease detection is temporarily unavailable") from exc

    return DiseaseResponse(
        disease=result["disease"],
        confidence=result["confidence"],
        low_confidence=result["low_confidence"],
        recommended_actions=result["actions"],
        language=language,
    )
