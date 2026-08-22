import logging

from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import WeatherResponse
from app.services import weather_service

logger = logging.getLogger("kisanai")
router = APIRouter()


@router.get("/weather", response_model=WeatherResponse)
def get_weather(
    location: str = Query(..., min_length=1, max_length=200),
    crop: str | None = Query(default=None, max_length=100),
    language: str = Query(default="en", pattern="^(en|hi)$"),
):
    try:
        result = weather_service.get_weather(location, crop, language)
    except Exception as exc:  # noqa: BLE001
        logger.exception("weather service failed")
        raise HTTPException(status_code=502, detail="Weather service is temporarily unavailable") from exc

    return WeatherResponse(**result, language=language)
