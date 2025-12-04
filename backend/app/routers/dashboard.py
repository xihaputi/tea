from typing import List
from datetime import datetime, timedelta
from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import TeaGarden, Device, Alarm, User
from ..schemas import DashboardStats, ChartData

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    获取仪表盘统计数据
    Get dashboard statistics
    """
    # 基础统计
    garden_count = db.query(TeaGarden).count()
    device_count = db.query(Device).count()
    device_online_count = db.query(Device).filter(Device.status == "online").count()
    alarm_count = db.query(Alarm).filter(Alarm.status == "active").count()
    user_count = db.query(User).count()
    
    # 告警趋势（最近7天）
    # Alarm trend (last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=6)
    
    # SQLite date formatting might differ, assuming standard SQL or handling in python
    # For simplicity/compatibility, let's query all recent alarms and aggregate in Python
    # Or use group_by if we are sure about the DB dialect. 
    # Since we are using SQLite in this env (usually), func.strftime is available.
    
    # 简单起见，这里先用 Python 处理日期聚合，避免 SQL 方言问题
    recent_alarms = db.query(Alarm).filter(Alarm.created_at >= start_date).all()
    
    date_map = {}
    for i in range(7):
        d = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        date_map[d] = 0
        
    for alarm in recent_alarms:
        d = alarm.created_at.strftime("%Y-%m-%d")
        if d in date_map:
            date_map[d] += 1
            
    alarm_trend = [ChartData(name=k, value=v) for k, v in date_map.items()]
    
    return DashboardStats(
        garden_count=garden_count,
        device_count=device_count,
        device_online_count=device_online_count,
        alarm_count=alarm_count,
        user_count=user_count,
        alarm_trend=alarm_trend
    )
