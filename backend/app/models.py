from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


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

