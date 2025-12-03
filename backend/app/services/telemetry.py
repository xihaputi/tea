from datetime import datetime
from typing import Dict, Any

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Telemetry, Device


def save_telemetry(sn: str, data: Dict[str, Any]):
    """
    MQTT 消息入库。
    根据 SN 查找设备，更新在线状态和最后上报时间。
    """
    db: Session = SessionLocal()
    try:
        # 1. 根据 SN 查找设备
        device = db.query(Device).filter(Device.sn == sn).first()
        if not device:
            print(f"[MQTT] Device not found for SN: {sn}")
            return

        # 2. 更新设备状态和时间
        device.status = "online"
        device.last_time = datetime.utcnow()
        db.add(device) # 标记更新

        # 3. 保存遥测数据
        for key, value in data.items():
            record = Telemetry(
                device_id=device.id,
                key=key,
                value=str(value),
                ts=datetime.utcnow(),
            )
            db.add(record)
        
        db.commit()
        print(f"[MQTT] Data saved for device: {device.name} ({sn})")

    except Exception as e:
        print(f"[MQTT] Error saving telemetry: {e}")
        db.rollback()
    finally:
        db.close()


def save_telemetry_http(device_id: int, payload: Dict[str, Any], db: Session):
    """HTTP 接口入库。"""
    device = db.query(Device).get(device_id)
    if not device:
        return False
    for key, value in payload.items():
        record = Telemetry(
            device_id=device_id,
            key=key,
            value=str(value),
            ts=datetime.utcnow(),
        )
        db.add(record)
    db.commit()
    return True
