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


# Auth
class LoginRequest(BaseModel):
    username: str
    password: str
    captchaKey: Optional[str] = None
    captchaCode: Optional[str] = None


class UserInfo(BaseModel):
    id: int
    name: str
    avatar: Optional[str] = None
    roles: List[str] = []


class LoginResponse(BaseModel):
    token: str
    userInfo: UserInfo


# Dashboard
class DashboardStats(BaseModel):
    gardenCount: int
    deviceCount: int
    alertCount: int
    onlineRate: float


# Tea garden
class TeaGardenCreate(BaseModel):
    name: str
    address: Optional[str] = None
    manager: Optional[str] = None
    company: Optional[str] = None
    area: Optional[float] = None
    desc: Optional[str] = None


class TeaGardenUpdate(TeaGardenCreate):
    status: Optional[str] = None


class TeaGardenOut(TeaGardenCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PageResult(BaseModel):
    list: List[TeaGardenOut]
    total: int


class PlotCreate(BaseModel):
    code: str
    variety: Optional[str] = None
    area: Optional[float] = None


class PlotOut(PlotCreate):
    id: int

    class Config:
        orm_mode = True


class DeviceCreate(BaseModel):
    name: str
    sn: str
    product_id: Optional[int] = None
    garden_id: Optional[int] = None
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    sn: Optional[str] = None
    product_id: Optional[int] = None
    garden_id: Optional[int] = None
    status: Optional[str] = None
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None


class DeviceOut(DeviceCreate):
    id: int
    status: str
    last_time: datetime

    class Config:
        orm_mode = True


class RuleCreate(BaseModel):
    name: str
    condition: Optional[str] = None
    actions: Optional[str] = None


class RuleOut(RuleCreate):
    id: int
    enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
