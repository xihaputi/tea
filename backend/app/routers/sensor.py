from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from ..schemas import SensorRecordOut

router = APIRouter(prefix="/sensor", tags=["sensor"])

_now = datetime.now(timezone.utc)
# 模拟传感器数据
# Mock sensor data
_sensor_data: List[SensorRecordOut] = [
    SensorRecordOut(plot_id=1, soil_moisture=25.0, temperature=22.3, humidity=68.0, timestamp=_now - timedelta(hours=2)),
    SensorRecordOut(plot_id=1, soil_moisture=32.5, temperature=23.0, humidity=65.0, timestamp=_now),
    SensorRecordOut(plot_id=2, soil_moisture=71.5, temperature=21.5, humidity=70.0, timestamp=_now - timedelta(hours=1)),
]


def _get_latest_sensor(plot_id: int) -> Optional[SensorRecordOut]:
    """
    获取指定地块的最新传感器数据（内部辅助函数）
    Get latest sensor data for a plot (internal helper)
    """
    data = [record for record in _sensor_data if record.plot_id == plot_id]
    return data[-1] if data else None


@router.get("/latest", response_model=SensorRecordOut)
def get_latest_sensor(plot_id: int = Query(..., gt=0)) -> SensorRecordOut:
    """
    获取最新传感器数据
    Get latest sensor data
    """
    latest = _get_latest_sensor(plot_id)
    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data for this plot")
    return latest


@router.get("/history", response_model=List[SensorRecordOut])
def get_sensor_history(
    plot_id: int = Query(..., gt=0),
    period: str = Query("7d", description="Time span like 7d or 24h for mock filtering"),
) -> List[SensorRecordOut]:
    """
    获取传感器历史数据
    Get sensor history data
    """
    # 模拟过滤：目前返回所有条目
    # Mock filtering: return all entries for now.
    history = [record for record in _sensor_data if record.plot_id == plot_id]
    if not history:
        raise HTTPException(status_code=404, detail="No sensor data for this plot")
    return history
