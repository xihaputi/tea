from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


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

    garden = relationship("TeaGarden", back_populates="devices")


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
    condition = Column(Text, nullable=True)         # 触发条件 / Trigger Condition
    actions = Column(Text, nullable=True)           # 执行动作 / Actions
    enabled = Column(Boolean, default=True)         # 是否启用 / Enabled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
