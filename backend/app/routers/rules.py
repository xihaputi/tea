from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Rule
from ..schemas import RuleCreate, RuleOut

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("", response_model=dict)
def list_rules(page: int = Query(1, ge=1), size: int = Query(10, ge=1), db: Session = Depends(get_db)):
    """
    获取规则列表
    Get rule list
    """
    query = db.query(Rule)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"list": items, "total": total}


@router.post("", response_model=RuleOut)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
    """
    创建规则
    Create rule
    """
    rule = Rule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.put("/{rule_id}", response_model=RuleOut)
def update_rule(rule_id: int, payload: RuleCreate, db: Session = Depends(get_db)):
    """
    更新规则
    Update rule
    """
    rule = db.query(Rule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(rule, k, v)
    db.commit()
    db.refresh(rule)
    return rule


@router.put("/{rule_id}/enable")
def enable_rule(rule_id: int, enabled: bool, db: Session = Depends(get_db)):
    """
    启用/禁用规则
    Enable/Disable rule
    """
    rule = db.query(Rule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    rule.enabled = enabled
    db.commit()
    return {"success": True}


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    删除规则
    Delete rule
    """
    rule = db.query(Rule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(rule)
    db.commit()
    return {"success": True}


# Sensor Rule Endpoints

from typing import List
from ..models import SensorRule
from ..schemas import SensorRuleCreate, SensorRuleOut

@router.get("/sensor", response_model=List[SensorRuleOut])
def list_sensor_rules(db: Session = Depends(get_db)):
    """获取传感器状态规则列表"""
    return db.query(SensorRule).all()

@router.post("/sensor", response_model=SensorRuleOut)
def create_sensor_rule(payload: SensorRuleCreate, db: Session = Depends(get_db)):
    """创建传感器状态规则"""
    exists = db.query(SensorRule).filter(SensorRule.sensor_key == payload.sensor_key).first()
    if exists:
        raise HTTPException(status_code=400, detail=f"Rule for sensor key '{payload.sensor_key}' already exists")
    
    rule = SensorRule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.put("/sensor/{rule_id}", response_model=SensorRuleOut)
def update_sensor_rule(rule_id: int, payload: SensorRuleCreate, db: Session = Depends(get_db)):
    """更新传感器状态规则"""
    rule = db.query(SensorRule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    
    if payload.sensor_key != rule.sensor_key:
        exists = db.query(SensorRule).filter(SensorRule.sensor_key == payload.sensor_key).first()
        if exists:
             raise HTTPException(status_code=400, detail=f"Rule for sensor key '{payload.sensor_key}' already exists")

    rule.name = payload.name
    rule.sensor_key = payload.sensor_key
    rule.rule_config = payload.rule_config
    
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/sensor/{rule_id}")
def delete_sensor_rule(rule_id: int, db: Session = Depends(get_db)):
    """删除传感器状态规则"""
    rule = db.query(SensorRule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(rule)
    db.commit()
    return {"success": True}

