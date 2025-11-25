from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PlotBase(BaseModel):
    name: str
    location: Optional[str] = None
    status: Optional[str] = Field(default="unknown", description="Current plot status")


class PlotCreate(PlotBase):
    pass


class PlotOut(PlotBase):
    id: int

    class Config:
        orm_mode = True


class SensorRecordBase(BaseModel):
    plot_id: int
    soil_moisture: float = Field(..., ge=0, le=100)
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class SensorRecordOut(SensorRecordBase):
    timestamp: datetime

    class Config:
        orm_mode = True


class AdviceOut(BaseModel):
    plot_id: int
    soil_moisture: float
    level: str
    advice: str
    timestamp: datetime

    class Config:
        orm_mode = True


class DiseasePrediction(BaseModel):
    disease_type: str
    confidence: float
    advice: str
    image_url: Optional[str] = None
    plot_id: Optional[int] = None
    timestamp: datetime


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    plot_id: Optional[int] = None
    question: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    answer: str

