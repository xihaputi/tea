from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from ..schemas import AdviceOut
from ..services.rule_engine import evaluate_soil_moisture
from .sensor import _get_latest_sensor

router = APIRouter(prefix="/advice", tags=["advice"])


@router.get("/today", response_model=AdviceOut)
def get_today_advice(plot_id: int = Query(..., gt=0)) -> AdviceOut:
    latest = _get_latest_sensor(plot_id)
    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data for this plot")

    decision = evaluate_soil_moisture(latest.soil_moisture)
    return AdviceOut(
        plot_id=plot_id,
        soil_moisture=latest.soil_moisture,
        level=decision["level"],
        advice=decision["advice"],
        timestamp=datetime.now(timezone.utc),
    )

