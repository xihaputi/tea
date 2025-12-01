from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Device, Product, TeaGarden, Telemetry
from ..schemas import DeviceCreate, DeviceOut, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    """
    获取产品列表（设备类型）
    Get product list (device types)
    """
    products = db.query(Product).all()
    if not products:
        # 初始化默认产品数据
        # Initialize default product data
        default = [
            Product(id=1, name="土壤传感器 v1", parent_id=None),
            Product(id=2, name="茶园气象站 v2", parent_id=None),
            Product(id=3, name="水肥一体机", parent_id=None),
        ]
        db.add_all(default)
        db.commit()
        products = db.query(Product).all()
    return [{"id": p.id, "label": p.name, "parentId": p.parent_id} for p in products]


@router.get("", response_model=dict)
def list_devices(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    productId: Optional[int] = None,
    gardenId: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    获取设备列表，支持分页和筛选
    Get device list with pagination and filtering
    """
    query = db.query(Device)
    if keyword:
        query = query.filter(Device.name.like(f"%{keyword}%"))
    if status:
        query = query.filter(Device.status == status)
    if productId:
        query = query.filter(Device.product_id == productId)
    if gardenId is not None:
        # 如果传 -1，表示查询未绑定的设备
        # If -1, query unbound devices
        if gardenId == -1:
            query = query.filter(Device.garden_id == None)
        else:
            query = query.filter(Device.garden_id == gardenId)
            
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"list": items, "total": total}


@router.post("", response_model=DeviceOut)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    """
    创建新设备
    Create new device
    """
    device = Device(**payload.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.put("/{device_id}")
def update_device(device_id: int, payload: DeviceUpdate, db: Session = Depends(get_db)):
    """
    更新设备信息
    Update device information
    """
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Not found")
        
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(device, k, v)
        
    db.commit()
    return {"success": True}


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """
    获取设备详情
    Get device details
    """
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Not found")
    return device


@router.get("/{device_id}/telemetry")
def get_latest_telemetry(device_id: int, db: Session = Depends(get_db)):
    """
    获取设备最新遥测数据
    Get latest telemetry data for device
    """
    latest = (
        db.query(Telemetry)
        .filter(Telemetry.device_id == device_id)
        .order_by(Telemetry.ts.desc())
        .limit(10)
        .all()
    )
    return [{"ts": t.ts, "key": t.key, "value": t.value} for t in latest]


@router.get("/{device_id}/telemetry/history")
def get_telemetry_history(
    device_id: int,
    startTs: Optional[datetime] = None,
    endTs: Optional[datetime] = None,
    keys: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取设备历史遥测数据
    Get historical telemetry data for device
    """
    query = db.query(Telemetry).filter(Telemetry.device_id == device_id)
    if startTs:
        query = query.filter(Telemetry.ts >= startTs)
    if endTs:
        query = query.filter(Telemetry.ts <= endTs)
    if keys:
        key_list = [k.strip() for k in keys.split(",")]
        query = query.filter(Telemetry.key.in_(key_list))
    rows = query.order_by(Telemetry.ts.desc()).limit(100).all()
    result = {}
    for r in rows:
        result.setdefault(r.key, []).append({"ts": r.ts, "value": r.value})
    return result
