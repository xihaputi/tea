from sqlalchemy.orm import Session
from ..models import Rule, Alarm, Device
from datetime import datetime

def evaluate_telemetry(db: Session, device_id: int, telemetry: dict):
    """
    评估设备遥测数据，触发规则
    Evaluate device telemetry and trigger rules
    """
    # 1. 获取设备信息
    device = db.query(Device).get(device_id)
    if not device:
        return

    # 2. 获取适用于该设备的所有启用规则
    # 规则可以是绑定到特定设备的，也可以是绑定到产品类型的
    rules = db.query(Rule).filter(
        Rule.enabled == True,
        ((Rule.device_id == device_id) | 
         ((Rule.product_id == device.product_id) & (Rule.device_id == None)))
    ).all()
    
    for rule in rules:
        check_rule(db, rule, device, telemetry)

def check_rule(db: Session, rule: Rule, device: Device, telemetry: dict):
    """
    检查单个规则
    Check single rule
    """
    # 简单规则：检查 input_key 是否存在于遥测数据中
    if not rule.input_key or rule.input_key not in telemetry:
        return
        
    value = telemetry[rule.input_key]
    
    # 尝试将值转换为 float 进行比较
    try:
        val_num = float(value)
    except (ValueError, TypeError):
        return # 非数字暂不处理
        
    triggered = False
    
    if rule.operator == ">":
        triggered = val_num > rule.threshold
    elif rule.operator == "<":
        triggered = val_num < rule.threshold
    elif rule.operator == ">=":
        triggered = val_num >= rule.threshold
    elif rule.operator == "<=":
        triggered = val_num <= rule.threshold
    elif rule.operator == "=":
        triggered = val_num == rule.threshold
        
    if triggered:
        trigger_alarm(db, rule, device, val_num)
    else:
        # 如果规则未触发，检查是否需要自动清除告警（可选）
        pass

def trigger_alarm(db: Session, rule: Rule, device: Device, value: float):
    """
    触发告警
    Trigger alarm
    """
    # 检查是否已有未清除的同类告警
    existing_alarm = db.query(Alarm).filter(
        Alarm.device_id == device.id,
        Alarm.rule_id == rule.id,
        Alarm.status != "cleared"
    ).first()
    
    if existing_alarm:
        # 更新现有告警时间
        existing_alarm.updated_at = datetime.utcnow()
        existing_alarm.content = f"规则触发: {rule.name} (当前值: {value})"
    else:
        # 创建新告警
        new_alarm = Alarm(
            device_id=device.id,
            rule_id=rule.id,
            severity="warning",
            content=f"规则触发: {rule.name} (当前值: {value})",
            status="active"
        )
        db.add(new_alarm)
    
    db.commit()


def evaluate_soil_moisture(soil_moisture: float) -> dict:
    """Very simple rule engine for irrigation advice (Legacy support)."""
    if soil_moisture < 30:
        return {"level": "water", "advice": "Soil is dry, schedule watering today."}
    if 30 <= soil_moisture <= 70:
        return {"level": "optimal", "advice": "Moisture is within the optimal range."}
    return {"level": "drain", "advice": "Soil is too wet, pause watering and check drainage."}


