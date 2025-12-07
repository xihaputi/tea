from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship

from .database import Base

# 用户-茶园关联表
user_gardens = Table(
    "user_gardens",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("garden_id", Integer, ForeignKey("tea_gardens.id"), primary_key=True),
)

class User(Base):
    """
    用户模型
    User Model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)  # 用户名 / Username
    password = Column(String(128), nullable=False)  # 密码（演示用明文） / Password (plain text for demo)
    name = Column(String(100), nullable=False)      # 姓名 / Name
    avatar = Column(String(255), nullable=True)     # 头像 URL / Avatar URL
    roles = Column(String(255), nullable=True)      # 角色（逗号分隔） / Roles (comma separated)
    permissions = Column(Text, nullable=True)       # 权限列表 (JSON) / Permissions (JSON)

    gardens = relationship("TeaGarden", secondary=user_gardens, backref="users")


class GardenPlot(Base):
    """
    地块模型（旧版，建议使用 Plot）
    Garden Plot Model (Legacy, recommend using Plot)
    """
    __tablename__ = "garden_plots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)
    status = Column(String(50), default="unknown")

    sensor_records = relationship("SensorRecord", back_populates="plot")
    advice_records = relationship("AdviceRecord", back_populates="plot")
    disease_records = relationship("DiseaseRecord", back_populates="plot")



class SensorRecord(Base):
    """
    传感器记录模型
    Sensor Record Model
    """
    __tablename__ = "sensor_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("garden_plots.id"))
    soil_moisture = Column(Float, nullable=False)  # 土壤湿度 / Soil Moisture
    temperature = Column(Float, nullable=True)     # 温度 / Temperature
    humidity = Column(Float, nullable=True)        # 湿度 / Humidity
    timestamp = Column(DateTime, default=datetime.utcnow) # 时间戳 / Timestamp

    plot = relationship("GardenPlot", back_populates="sensor_records")


class AdviceRecord(Base):
    """
    农事建议记录模型
    Farming Advice Record Model
    """
    __tablename__ = "advice_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("garden_plots.id"))
    soil_moisture = Column(Float, nullable=False)
    level = Column(String(50), nullable=False)  # 建议等级 / Advice Level
    advice = Column(Text, nullable=False)       # 建议内容 / Advice Content
    timestamp = Column(DateTime, default=datetime.utcnow)

    plot = relationship("GardenPlot", back_populates="advice_records")


class DiseaseRecord(Base):
    """
    病虫害识别记录模型
    Disease Detection Record Model
    """
    __tablename__ = "disease_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("garden_plots.id"), nullable=True)
    image_path = Column(String(255), nullable=False)  # 图片路径 / Image Path
    disease_type = Column(String(100), nullable=False) # 病害类型 / Disease Type
    confidence = Column(Float, nullable=False)        # 置信度 / Confidence
    advice = Column(Text, nullable=False)             # 防治建议 / Treatment Advice
    timestamp = Column(DateTime, default=datetime.utcnow)

    plot = relationship("GardenPlot", back_populates="disease_records")


class TeaGarden(Base):
    """
    茶园模型
    Tea Garden Model
    """
    __tablename__ = "tea_gardens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)      # 茶园名称 / Garden Name
    address = Column(String(255), nullable=True)    # 地址 / Address
    manager = Column(String(100), nullable=True)    # 负责人 / Manager
    company = Column(String(100), nullable=True)    # 所属公司 / Company

    area = Column(Float, nullable=True)             # 面积 / Area
    desc = Column(Text, nullable=True)              # 描述 / Description
    latitude = Column(Float, nullable=True)         # 纬度 / Latitude
    longitude = Column(Float, nullable=True)        # 经度 / Longitude
    camera_url = Column(String(255), nullable=True) # 摄像头地址 / Camera URL
    image_path = Column(String(255), nullable=True) # 茶园封面图 / Garden Cover Image
    status = Column(String(50), default="active")   # 状态 / Status
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    plots = relationship("Plot", back_populates="garden")
    devices = relationship("Device", back_populates="garden")


class Plot(Base):
    """
    地块模型（新版）
    Plot Model (New)
    """
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    garden_id = Column(Integer, ForeignKey("tea_gardens.id"))
    code = Column(String(50), nullable=False)       # 地块编号 / Plot Code
    variety = Column(String(100), nullable=True)    # 茶树品种 / Tea Variety
    area = Column(Float, nullable=True)             # 面积 / Area
    created_at = Column(DateTime, default=datetime.utcnow)

    garden = relationship("TeaGarden", back_populates="plots")


class Product(Base):
    """
    产品模型（设备类型）
    Product Model (Device Type)
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)      # 产品名称 / Product Name
    parent_id = Column(Integer, ForeignKey("products.id"), nullable=True) # 父级ID / Parent ID


class Device(Base):
    """
    设备模型
    Device Model
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    garden_id = Column(Integer, ForeignKey("tea_gardens.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    name = Column(String(100), nullable=False)      # 设备名称 / Device Name
    sn = Column(String(100), unique=True, nullable=False) # 序列号 / Serial Number
    mqtt_username = Column(String(100), nullable=True) # MQTT 用户名 / MQTT Username
    mqtt_password = Column(String(100), nullable=True) # MQTT 密码 / MQTT Password
    status = Column(String(50), default="offline")  # 状态 / Status
    last_time = Column(DateTime, default=datetime.utcnow) # 最后在线时间 / Last Online Time
    sensor_config = Column(Text, nullable=True) # 传感器配置 (JSON) / Sensor Config

    garden = relationship("TeaGarden", back_populates="devices")
    alarms = relationship("Alarm", back_populates="device")


class Telemetry(Base):
    """
    遥测数据模型
    Telemetry Data Model
    """
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    ts = Column(DateTime, default=datetime.utcnow)  # 时间戳 / Timestamp
    key = Column(String(50), nullable=False)        # 数据键 / Data Key
    value = Column(String(100), nullable=False)     # 数据值 / Data Value


class Rule(Base):
    """
    规则模型
    Rule Model
    """
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)      # 规则名称 / Rule Name
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True) # 关联产品 / Related Product
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)   # 关联设备（可选）/ Related Device (Optional)
    
    # 简单规则定义
    input_key = Column(String(50), nullable=True)   # 监控字段 (e.g. temperature)
    operator = Column(String(10), nullable=True)    # 操作符 (>, <, =, >=, <=)
    threshold = Column(Float, nullable=True)        # 阈值
    
    condition = Column(Text, nullable=True)         # 复杂条件（保留字段）
    actions = Column(Text, nullable=True)           # 执行动作 (JSON)
    enabled = Column(Boolean, default=True)         # 是否启用
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Alarm(Base):
    """
    告警模型
    Alarm Model
    """
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("rules.id"), nullable=True)
    
    severity = Column(String(20), default="warning") # 告警级别: info, warning, critical
    content = Column(String(255), nullable=False)    # 告警内容
    status = Column(String(20), default="active")    # 状态: active, acknowledged, cleared
    
    created_at = Column(DateTime, default=datetime.utcnow) # 发生时间
    updated_at = Column(DateTime, default=datetime.utcnow) # 更新时间
    cleared_at = Column(DateTime, nullable=True)           # 清除时间
    handler_id = Column(Integer, ForeignKey("users.id"), nullable=True) # 处理人ID

    device = relationship("Device", back_populates="alarms")
    rule = relationship("Rule")
    handler = relationship("User") # 关联处理人


class Task(Base):
    """
    计划任务/定时任务模型
    Scheduled/Plan Task Model
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)      # 任务名称 / Task Name
    type = Column(String(50), default="cron")       # 类型: cron, once, plan
    cron = Column(String(100), nullable=True)       # Cron 表达式 / Cron Expression
    
    target_type = Column(String(50), nullable=True) # 目标类型: device, garden, system
    target_id = Column(Integer, nullable=True)      # 目标ID
    
    action_type = Column(String(50), nullable=True) # 动作类型: control, notify, report
    action_data = Column(Text, nullable=True)       # 动作数据 (JSON)
    
    enabled = Column(Boolean, default=True)         # 是否启用
    status = Column(String(50), default="idle")     # 状态: idle, running, failed, last_success
    
    last_run = Column(DateTime, nullable=True)      # 上次执行时间
    next_run = Column(DateTime, nullable=True)      # 下次执行时间
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class SensorRule(Base):
    """
    传感器状态映射规则 (用于状态显示)
    Sensor Status Mapping Rule
    """
    __tablename__ = "sensor_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)      # 规则名称 (e.g. 土壤水分判断标准)
    sensor_key = Column(String(100), unique=True, index=True, nullable=False) # 传感器 Key (e.g. soil_humi)
    rule_config = Column(Text, nullable=False)      # 规则配置 (JSON format)
                                                    # e.g. [{"min":0, "max":50, "label":"干旱", "color":"#f56c6c"}]
    created_at = Column(DateTime, default=datetime.utcnow)



class ChatSession(Base):
    """
    聊天会话模型
    Chat Session Model
    """
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=True)     # 会话标题 / Session Title
    created_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """
    聊天记录模型
    Chat Message Model
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)      # user / assistant / system
    content = Column(Text, nullable=False)         # 内容 / Content
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
