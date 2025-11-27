from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)  # plain for demo
    name = Column(String(100), nullable=False)
    avatar = Column(String(255), nullable=True)
    roles = Column(String(255), nullable=True)


class GardenPlot(Base):
    __tablename__ = "garden_plots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)
    status = Column(String(50), default="unknown")

    sensor_records = relationship("SensorRecord", back_populates="plot")
    advice_records = relationship("AdviceRecord", back_populates="plot")
    disease_records = relationship("DiseaseRecord", back_populates="plot")



class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("garden_plots.id"))
    soil_moisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    plot = relationship("GardenPlot", back_populates="sensor_records")


class AdviceRecord(Base):
    __tablename__ = "advice_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("garden_plots.id"))
    soil_moisture = Column(Float, nullable=False)
    level = Column(String(50), nullable=False)
    advice = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    plot = relationship("GardenPlot", back_populates="advice_records")


class DiseaseRecord(Base):
    __tablename__ = "disease_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("garden_plots.id"), nullable=True)
    image_path = Column(String(255), nullable=False)
    disease_type = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    advice = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    plot = relationship("GardenPlot", back_populates="disease_records")


class TeaGarden(Base):
    __tablename__ = "tea_gardens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=True)
    manager = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    area = Column(Float, nullable=True)
    desc = Column(Text, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    plots = relationship("Plot", back_populates="garden")
    devices = relationship("Device", back_populates="garden")


class Plot(Base):
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    garden_id = Column(Integer, ForeignKey("tea_gardens.id"))
    code = Column(String(50), nullable=False)
    variety = Column(String(100), nullable=True)
    area = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    garden = relationship("TeaGarden", back_populates="plots")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("products.id"), nullable=True)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    garden_id = Column(Integer, ForeignKey("tea_gardens.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    name = Column(String(100), nullable=False)
    sn = Column(String(100), unique=True, nullable=False)
    mqtt_username = Column(String(100), nullable=True)
    mqtt_password = Column(String(100), nullable=True)
    status = Column(String(50), default="offline")
    last_time = Column(DateTime, default=datetime.utcnow)

    garden = relationship("TeaGarden", back_populates="devices")


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    ts = Column(DateTime, default=datetime.utcnow)
    key = Column(String(50), nullable=False)
    value = Column(String(100), nullable=False)


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    condition = Column(Text, nullable=True)
    actions = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
