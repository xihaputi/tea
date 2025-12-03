from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PlotBase(BaseModel):
    """地块基础模型 / Plot Base Model"""
    name: str
    location: Optional[str] = None
    status: Optional[str] = Field(default="unknown", description="Current plot status")


class PlotCreate(PlotBase):
    """地块创建模型 / Plot Create Model"""
    pass


class PlotOut(PlotBase):
    """地块输出模型 / Plot Output Model"""
    id: int

    class Config:
        orm_mode = True


class SensorRecordBase(BaseModel):
    """传感器记录基础模型 / Sensor Record Base Model"""
    plot_id: int
    soil_moisture: float = Field(..., ge=0, le=100)
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class SensorRecordOut(SensorRecordBase):
    """传感器记录输出模型 / Sensor Record Output Model"""
    timestamp: datetime

    class Config:
        orm_mode = True


class AdviceOut(BaseModel):
    """农事建议输出模型 / Advice Output Model"""
    plot_id: int
    soil_moisture: float
    level: str
    advice: str
    timestamp: datetime

    class Config:
        orm_mode = True


class DiseasePrediction(BaseModel):
    """病害预测模型 / Disease Prediction Model"""
    disease_type: str
    confidence: float
    advice: str
    image_url: Optional[str] = None
    plot_id: Optional[int] = None
    timestamp: datetime


class ChatMessage(BaseModel):
    """聊天消息模型 / Chat Message Model"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """聊天请求模型 / Chat Request Model"""
    plot_id: Optional[int] = None
    question: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    """聊天响应模型 / Chat Response Model"""
    answer: str


# Auth
class LoginRequest(BaseModel):
    """登录请求模型 / Login Request Model"""
    username: str
    password: str
    captchaKey: Optional[str] = None
    captchaCode: Optional[str] = None


class UserInfo(BaseModel):
    """用户信息模型 / User Info Model"""
    id: int
    name: str
    avatar: Optional[str] = None
    roles: List[str] = []


class LoginResponse(BaseModel):
    """登录响应模型 / Login Response Model"""
    token: str
    userInfo: UserInfo


# Dashboard
class DashboardStats(BaseModel):
    """仪表盘统计模型 / Dashboard Stats Model"""
    gardenCount: int
    deviceCount: int
    alertCount: int
    onlineRate: float


# Tea garden
class TeaGardenCreate(BaseModel):
    """茶园创建模型 / Tea Garden Create Model"""
    name: str
    address: Optional[str] = None
    manager: Optional[str] = None
    company: Optional[str] = None
    area: Optional[float] = None
    desc: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    camera_url: Optional[str] = None


class TeaGardenUpdate(TeaGardenCreate):
    """茶园更新模型 / Tea Garden Update Model"""
    status: Optional[str] = None


class TeaGardenOut(TeaGardenCreate):
    """茶园输出模型 / Tea Garden Output Model"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    # 统计字段
    plotCount: int = 0
    totalCount: int = 0
    onlineCount: int = 0

    class Config:
        orm_mode = True


class PageResult(BaseModel):
    """分页结果模型 / Page Result Model"""
    list: List[TeaGardenOut]
    total: int


class PlotCreate(BaseModel):
    """地块创建模型（新版） / Plot Create Model"""
    code: str
    variety: Optional[str] = None
    area: Optional[float] = None


class PlotOut(PlotCreate):
    """地块输出模型（新版） / Plot Output Model"""
    id: int

    class Config:
        orm_mode = True


class DeviceCreate(BaseModel):
    """设备创建模型 / Device Create Model"""
    name: str
    sn: str
    product_id: Optional[int] = None
    garden_id: Optional[int] = None
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    sensor_config: Optional[str] = None


class DeviceUpdate(BaseModel):
    """设备更新模型 / Device Update Model"""
    name: Optional[str] = None
    sn: Optional[str] = None
    product_id: Optional[int] = None
    garden_id: Optional[int] = None
    status: Optional[str] = None
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    sensor_config: Optional[str] = None


    class Config:
        orm_mode = True

class DeviceOut(DeviceCreate):
    """设备输出模型 / Device Output Model"""
    id: int
    status: str
    last_time: datetime
    productName: Optional[str] = None

    class Config:
        orm_mode = True


class RuleCreate(BaseModel):
    """规则创建模型 / Rule Create Model"""
    name: str
    condition: Optional[str] = None
    actions: Optional[str] = None


class RuleOut(RuleCreate):
    """规则输出模型 / Rule Output Model"""
    id: int
    enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
