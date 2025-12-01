from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Device, TeaGarden
from ..schemas import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    """
    获取仪表盘统计数据
    Get dashboard statistics
    """
    gardens = db.query(TeaGarden).count()
    devices = db.query(Device).count()
    # 演示数据
    # demo values
    return DashboardStats(
        gardenCount=gardens,
        deviceCount=devices,
        alertCount=3,
        onlineRate=0.85,
    )
