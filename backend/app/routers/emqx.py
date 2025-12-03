from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Device
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["emqx-auth"])

class AuthRequest(BaseModel):
    username: str
    password: str
    clientid: str

@router.post("/mqtt", status_code=200)
def mqtt_auth(req: AuthRequest, db: Session = Depends(get_db)):
    """
    EMQX HTTP Auth Hook
    Return 200 to allow, 4xx/5xx to deny.
    """
    # 1. Check for Backend Service (Super Admin)
    if req.username == settings.MQTT_USERNAME:
        if req.password == settings.MQTT_PASSWORD:
            return {"result": "allow", "is_superuser": True}
        else:
            raise HTTPException(status_code=401, detail="Invalid backend credentials")

    # 2. Check for Devices
    # Username should be the Device SN (or we can stick to a convention, but SN is unique)
    # Let's assume the device uses its SN as username, and the password configured in DB.
    
    # However, the user said "input correct account and password".
    # In `Device` model we have `mqtt_username` and `mqtt_password`.
    
    device = db.query(Device).filter(Device.mqtt_username == req.username).first()
    if not device:
        raise HTTPException(status_code=401, detail="Device not found")

    if device.mqtt_password != req.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"result": "allow", "is_superuser": False}
