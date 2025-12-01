from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Query

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
def get_stats_summary(plot_id: int = Query(..., gt=0)) -> Dict[str, Any]:
    """
    获取统计摘要
    Get stats summary
    """
    now = datetime.now(timezone.utc)
    return {
        "plot_id": plot_id,
        "average_soil_moisture": 48.3,
        "disease_events_last_30d": 1,
        "last_updated": now.isoformat(),
    }


@router.get("/uptime")
def healthcheck() -> Dict[str, str]:
    """
    健康检查
    Health check
    """
    return {"status": "ok", "timestamp": (datetime.now(timezone.utc) - timedelta(seconds=0)).isoformat()}
