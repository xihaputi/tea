from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Device, Product, TeaGarden, Telemetry, User
from ..schemas import DeviceCreate, DeviceOut, DeviceUpdate
from ..services.telemetry import save_telemetry_http
from ..dependencies import check_super_admin, get_current_active_user, is_super_admin, verify_garden_access

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
        default = [
            Product(id=1, name="土壤检测仪", parent_id=None),
            Product(id=2, name="茶园气象站", parent_id=None),
            Product(id=3, name="水肥一体机", parent_id=None),
            Product(id=4, name="阀门", parent_id=None),
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
    user: User = Depends(get_current_active_user),
):
    """
    获取设备列表，支持分页和筛选 (权限控制)
    """
    query = db.query(Device)
    
    # 权限过滤
    if not is_super_admin(user):
        assigned_ids = [g.id for g in user.gardens]
        if not assigned_ids:
             # 如果是非超管且无关联茶园，则只能看到空列表 (或者是否允许看 unbound? 暂定不允许)
             return {"list": [], "total": 0}
        # Filter: Device must be in assigned gardens
        query = query.filter(Device.garden_id.in_(assigned_ids))

    if keyword:
        query = query.filter(Device.name.like(f"%{keyword}%"))
    if status:
        query = query.filter(Device.status == status)
    if productId:
        query = query.filter(Device.product_id == productId)
    if gardenId is not None:
        if gardenId == -1:
            # 查询未绑定设备: 仅超管可见? or throw error if not super admin?
            # 简单处理：如果是普通用户查 -1，上面 assigned_ids 过滤已经排除 garden_id=None 的了(因为 None not in assigned_ids)
            # 但 Query filter 逻辑是 AND. garden_id=None AND garden_id in [1,2]. Result empty. Correct.
            query = query.filter(Device.garden_id == None)
        else:
            query = query.filter(Device.garden_id == gardenId)
            
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    # 手动填充 productName
    result_list = []
    for device in items:
        out = DeviceOut.from_orm(device)
        if device.product_id:
            product = db.query(Product).get(device.product_id)
            if product:
                out.productName = product.name
        result_list.append(out)
        
    return {"list": result_list, "total": total}


@router.post("", response_model=DeviceOut)
def create_device(
    payload: DeviceCreate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    """
    创建新设备 (需要管理权限)
    """
    if payload.garden_id:
        verify_garden_access(payload.garden_id, user, require_manage=True)
    else:
        # 创建未绑定茶园的设备: 仅超级管理员
        if not is_super_admin(user):
            raise HTTPException(status_code=403, detail="权限不足: 仅超级管理员可创建未绑定设备")

    device = Device(**payload.dict())
    
    # Auto-fill sensor config based on product
    import json
    if not device.sensor_config:
        if device.product_id == 1: # Soil
            config = {
                "soil_humi": {"name": "土壤含水量", "unit": "%", "show": True},
                "soil_temp": {"name": "土壤温度", "unit": "℃", "show": True},
                "soil_ph": {"name": "土壤PH", "unit": "", "show": True},
                "soil_ec": {"name": "土壤EC", "unit": "us/cm", "show": True}
            }
            device.sensor_config = json.dumps(config, ensure_ascii=False)
        elif device.product_id == 2: # Weather
            config = {
                "air_temp": {"name": "空气温度", "unit": "℃", "show": True},
                "humidity": {"name": "相对湿度", "unit": "%", "show": True},
                "rainfall": {"name": "降雨量", "unit": "mm", "show": True},
                "lux": {"name": "光照强度", "unit": "Lux", "show": True},
                "wind_speed": {"name": "风速", "unit": "m/s", "show": True},
                "wind_dir": {"name": "风向", "unit": "°", "show": True}
            }
            device.sensor_config = json.dumps(config, ensure_ascii=False)
            
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.put("/{device_id}")
def update_device(
    device_id: int, 
    payload: DeviceUpdate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    """
    更新设备信息 (需要管理权限)
    """
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Not found")
    
    # 检查对当前该设备所在茶园的权限
    if device.garden_id:
        verify_garden_access(device.garden_id, user, require_manage=True)
    else:
        if not is_super_admin(user):
            raise HTTPException(status_code=403, detail="权限不足: 无法管理未绑定设备")
            
    # 如果试图修改 garden_id (转移设备)，需要检查对 目标茶园 的权限
    if payload.garden_id is not None and payload.garden_id != device.garden_id:
        verify_garden_access(payload.garden_id, user, require_manage=True)

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(device, k, v)
        
    db.commit()
    return {"success": True}


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(
    device_id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    """
    获取设备详情
    """
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Not found")
        
    if device.garden_id:
        verify_garden_access(device.garden_id, user)
    else:
        if not is_super_admin(user):
             raise HTTPException(status_code=403, detail="权限不足")
             
    return device


@router.get("/{device_id}/telemetry")
def get_latest_telemetry(
    device_id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    """
    获取设备最新遥测数据
    """
    # 权限检查已在 get_device 逻辑类似
    device = db.query(Device).get(device_id)
    if not device:
         raise HTTPException(status_code=404, detail="Not found")
    if device.garden_id:
        verify_garden_access(device.garden_id, user)
    elif not is_super_admin(user):
        raise HTTPException(status_code=403, detail="权限不足")

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
    user: User = Depends(get_current_active_user)
):
    """
    获取设备历史遥测数据
    """
    device = db.query(Device).get(device_id)
    if not device:
         raise HTTPException(status_code=404, detail="Not found")
    if device.garden_id:
        verify_garden_access(device.garden_id, user)
    elif not is_super_admin(user):
        raise HTTPException(status_code=403, detail="权限不足")

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


@router.post("/{device_id}/telemetry")
def ingest_telemetry(device_id: int, payload: dict, db: Session = Depends(get_db)):
    """
    通过 HTTP 上报遥测，写入数据库
    注意：设备上报通常使用 device token 认证，这里暂时不强制 User 登录，
    或者假设设备网关有特殊的 auth。为保持简单，暂不加 User Depends。
    """
    ok = save_telemetry_http(device_id, payload, db)
    if not ok:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"success": True}


@router.delete("/{device_id}")
def delete_device(
    device_id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    """
    删除设备及其关联数据 (需要管理权限)
    """
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    if device.garden_id:
        verify_garden_access(device.garden_id, user, require_manage=True)
    else:
        if not is_super_admin(user):
            raise HTTPException(status_code=403, detail="权限不足")
        
    # 1. 删除关联的遥测数据
    db.query(Telemetry).filter(Telemetry.device_id == device_id).delete()
    
    # 2. 删除设备
    db.delete(device)
    db.commit()
    
    return {"success": True}
