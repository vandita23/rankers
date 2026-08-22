import logging

from fastapi import APIRouter, HTTPException, Query

from app.schemas.dashboard import DashboardResponse
from app.services import dashboard_service

logger = logging.getLogger("kisanai")
router = APIRouter()

# No auth in the current MVP — there's a single demo farmer row (id=1).
DEMO_FARMER_ID = 1


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(language: str = Query(default="en", pattern="^(en|hi)$")):
    try:
        result = dashboard_service.get_dashboard(DEMO_FARMER_ID, language)
    except Exception as exc:  # noqa: BLE001
        logger.exception("dashboard service failed")
        raise HTTPException(status_code=502, detail="Dashboard is temporarily unavailable") from exc

    return DashboardResponse(**result, language=language)
