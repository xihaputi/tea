from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import Task
from ..schemas import TaskBase, TaskCreate, TaskUpdate, TaskOut, TaskPageResult

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=TaskPageResult)
def get_task_list(
    page: int = 1,
    size: int = 10,
    name: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if name:
        query = query.filter(Task.name.like(f"%{name}%"))
    if type:
        query = query.filter(Task.type == type)
    
    total = query.count()
    tasks = query.offset((page - 1) * size).limit(size).all()
    
    return {"list": tasks, "total": total}

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_in.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"ok": True}

@router.post("/{task_id}/run")
def run_task_manually(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Placeholder for actual execution logic
    # In a real system, you would trigger the scheduler or execute the action here.
    # For now, we update the status and last_run
    task.status = "success"
    task.last_run = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return {"ok": True, "message": "Task triggered successfully (Simulated)"}
