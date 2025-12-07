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
    session_id: Optional[int] = None
    plot_id: Optional[int] = None
    question: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    """聊天响应模型 / Chat Response Model"""
    answer: str
    session_id: Optional[int] = None
    
class ChatSessionOut(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    class Config:
        orm_mode = True


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
    permissions: List[str] = []


class LoginResponse(BaseModel):
    """登录响应模型 / Login Response Model"""
    token: str
    userInfo: UserInfo


class UserCreate(BaseModel):
    """用户创建模型 / User Create Model"""
    username: str
    password: str
    name: str
    roles: List[str] = []
    garden_ids: List[int] = []
    permissions: List[str] = []


class UserUpdate(BaseModel):
    """用户更新模型 / User Update Model"""
    password: Optional[str] = None
    name: Optional[str] = None
    roles: List[str] = []
    garden_ids: List[int] = []
    permissions: List[str] = []


class UserOut(BaseModel):
    """用户输出模型 / User Output Model"""
    id: int
    username: str
    name: str
    roles: List[str] = []
    permissions: List[str] = []
    garden_ids: List[int] = []

    class Config:
        orm_mode = True


class UserPageResult(BaseModel):
    """用户分页结果模型 / User Page Result Model"""
    list: List[UserOut]
    total: int


# Dashboard
class ChartData(BaseModel):
    name: str
    value: int

class DashboardStats(BaseModel):
    """仪表盘统计模型 / Dashboard Stats Model"""
    garden_count: int
    device_count: int
    device_online_count: int
    alarm_count: int
    user_count: int
    alarm_trend: List[ChartData]


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
    image_path: Optional[str] = None


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
    alarmCount: int = 0

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
    product_id: Optional[int] = None
    device_id: Optional[int] = None
    input_key: Optional[str] = None
    operator: Optional[str] = None
    threshold: Optional[float] = None
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


class AlarmCreate(BaseModel):
    """告警创建模型 / Alarm Create Model"""
    device_id: int
    rule_id: Optional[int] = None
    severity: str
    content: str


class AlarmOut(AlarmCreate):
    """告警输出模型 / Alarm Output Model"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    cleared_at: Optional[datetime] = None
    
    # 关联信息
    deviceName: Optional[str] = None
    ruleName: Optional[str] = None
    gardenName: Optional[str] = None
    handlerName: Optional[str] = None # Adds handler name

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    """任务基础模型 / Task Base Model"""
    name: str
    type: Optional[str] = "cron"
    cron: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    action_type: Optional[str] = None
    action_data: Optional[str] = None
    enabled: bool = True

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    status: str
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TaskPageResult(BaseModel):
    list: List[TaskOut]
    total: int


class SensorRuleCreate(BaseModel):
    """传感器规则创建模型 / Sensor Rule Create Model"""
    name: str
    sensor_key: str
    rule_config: str  # JSON string

class SensorRuleOut(SensorRuleCreate):
    """传感器规则输出模型 / Sensor Rule Output Model"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


