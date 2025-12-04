from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Alarm, Device, Rule
from ..schemas import AlarmOut

router = APIRouter(prefix="/alarms", tags=["alarms"])


@router.get("", response_model=dict)
def list_alarms(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    status: Optional[str] = None,
    deviceId: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取告警列表
    Get alarm list
    """
    query = db.query(Alarm)
    if status:
        query = query.filter(Alarm.status == status)
    if deviceId:
        query = query.filter(Alarm.device_id == deviceId)
        
    total = query.count()
    items = query.order_by(Alarm.created_at.desc()).offset((page - 1) * size).limit(size).all()
    
    # 填充关联信息
    result = []
    for item in items:
        out = AlarmOut.from_orm(item)
        if item.device:
            out.deviceName = item.device.name
            if item.device.garden:
                out.gardenName = item.device.garden.name
        if item.rule:
            out.ruleName = item.rule.name
        result.append(out)
        
    return {"list": result, "total": total}


@router.put("/{alarm_id}/ack")
def acknowledge_alarm(alarm_id: int, db: Session = Depends(get_db)):
    """
    确认告警
    Acknowledge alarm
    """
    alarm = db.query(Alarm).get(alarm_id)
    if not alarm:
        raise HTTPException(status_code=404, detail="Not found")
        
    alarm.status = "acknowledged"
    alarm.updated_at = datetime.utcnow()
    db.commit()
    return {"success": True}


@router.put("/{alarm_id}/clear")
def clear_alarm(alarm_id: int, db: Session = Depends(get_db)):
    """
    清除告警
    Clear alarm
    """
    alarm = db.query(Alarm).get(alarm_id)
    if not alarm:
        raise HTTPException(status_code=404, detail="Not found")
        
    alarm.status = "cleared"
    alarm.cleared_at = datetime.utcnow()
    alarm.updated_at = datetime.utcnow()
    db.commit()
    return {"success": True}
