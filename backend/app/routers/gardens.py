from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Plot, TeaGarden
from ..schemas import PageResult, PlotCreate, PlotOut, TeaGardenCreate, TeaGardenOut, TeaGardenUpdate

router = APIRouter(prefix="/tea-gardens", tags=["tea-gardens"])


@router.get("", response_model=PageResult)
def list_gardens(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    company: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    获取茶园列表
    Get tea garden list
    """
    query = db.query(TeaGarden)
    if name:
        query = query.filter(TeaGarden.name.like(f"%{name}%"))
    if company:
        query = query.filter(TeaGarden.company == company)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return PageResult(list=items, total=total)


@router.post("", response_model=TeaGardenOut)
def create_garden(payload: TeaGardenCreate, db: Session = Depends(get_db)):
    """
    创建茶园
    Create tea garden
    """
    item = TeaGarden(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{garden_id}", response_model=TeaGardenOut)
def get_garden(garden_id: int, db: Session = Depends(get_db)):
    """
    获取茶园详情
    Get tea garden details
    """
    item = db.query(TeaGarden).get(garden_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@router.put("/{garden_id}")
def update_garden(garden_id: int, payload: TeaGardenUpdate, db: Session = Depends(get_db)):
    """
    更新茶园信息
    Update tea garden information
    """
    item = db.query(TeaGarden).get(garden_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    return {"success": True}


@router.delete("/{garden_id}")
def delete_garden(garden_id: int, db: Session = Depends(get_db)):
    """
    删除（停用）茶园
    Delete (deactivate) tea garden
    """
    item = db.query(TeaGarden).get(garden_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"success": True}


@router.get("/{garden_id}/plots", response_model=list[PlotOut])
def list_plots(garden_id: int, db: Session = Depends(get_db)):
    """
    获取茶园下的地块列表
    Get plot list for a tea garden
    """
    return db.query(Plot).filter(Plot.garden_id == garden_id).all()


@router.post("/{garden_id}/plots", response_model=PlotOut)
def create_plot(garden_id: int, payload: PlotCreate, db: Session = Depends(get_db)):
    """
    在茶园下创建地块
    Create plot in a tea garden
    """
    plot = Plot(garden_id=garden_id, **payload.dict())
    db.add(plot)
    db.commit()
    db.refresh(plot)
    return plot
