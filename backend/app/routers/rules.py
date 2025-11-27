from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Rule
from ..schemas import RuleCreate, RuleOut

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("", response_model=dict)
def list_rules(page: int = Query(1, ge=1), size: int = Query(10, ge=1), db: Session = Depends(get_db)):
    query = db.query(Rule)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"list": items, "total": total}


@router.post("", response_model=RuleOut)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
    rule = Rule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.put("/{rule_id}", response_model=RuleOut)
def update_rule(rule_id: int, payload: RuleCreate, db: Session = Depends(get_db)):
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
    rule = db.query(Rule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    rule.enabled = enabled
    db.commit()
    return {"success": True}


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(Rule).get(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(rule)
    db.commit()
    return {"success": True}
