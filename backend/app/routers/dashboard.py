from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Device, TeaGarden
from ..schemas import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    gardens = db.query(TeaGarden).count()
    devices = db.query(Device).count()
    # demo values
    return DashboardStats(
        gardenCount=gardens,
        deviceCount=devices,
        alertCount=3,
        onlineRate=0.85,
    )

