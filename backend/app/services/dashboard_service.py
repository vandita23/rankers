"""Dashboard aggregation service.

Reads the demo farmer, alerts and action plan from Supabase. If the
database isn't reachable (e.g. not configured yet during early dev), falls
back to static demo data so the frontend still renders — see PRD risk #23
("cache demo data and provide graceful fallback for the hackathon demo").
"""

import logging

from app.core.db import query

logger = logging.getLogger("kisanai")

_FALLBACK = {
    "farmer": {"name": "Ramesh", "location": "Barabanki, Uttar Pradesh", "crops": ["Wheat", "Sugarcane"]},
    "alerts": [
        {"id": "a1", "level": "warning", "text": "Rain expected in 2 days — delay pesticide spraying on wheat."},
        {"id": "a2", "level": "info", "text": "PM-KISAN next installment window opens this month."},
    ],
    "action_plan": [
        {"id": "p1", "done": False, "text": "Delay spraying — rain expected Thursday"},
        {"id": "p2", "done": False, "text": "Check wheat leaves for yellow rust spots"},
        {"id": "p3", "done": True, "text": "Irrigate sugarcane field (completed)"},
    ],
}


def get_dashboard(farmer_id: int, language: str) -> dict:
    name_col = "name_hi" if language == "hi" else "name"
    location_col = "location_hi" if language == "hi" else "location"
    crops_col = "crops_hi" if language == "hi" else "crops"
    text_col = "text_hi" if language == "hi" else "text_en"

    try:
        farmer_row = query(
            f"SELECT {name_col} AS name, {location_col} AS location, {crops_col} AS crops "
            f"FROM farmers WHERE id = %s",
            (farmer_id,),
            fetch="one",
        )
        alert_rows = query(
            f"SELECT id, level, {text_col} AS text FROM alerts "
            f"WHERE farmer_id = %s ORDER BY created_at DESC",
            (farmer_id,),
        )
        action_rows = query(
            f"SELECT id, done, {text_col} AS text FROM action_items "
            f"WHERE farmer_id = %s ORDER BY created_at ASC",
            (farmer_id,),
        )
        if not farmer_row:
            raise ValueError("farmer not found")
        return {
            "farmer": dict(farmer_row),
            "alerts": [{**dict(a), "id": str(a["id"])} for a in alert_rows],
            "action_plan": [{**dict(a), "id": str(a["id"])} for a in action_rows],
        }
    except Exception as exc:  # noqa: BLE001 - intentional broad fallback for demo resilience
        logger.warning("Dashboard DB read failed, using fallback data: %s", exc)
        return _FALLBACK
