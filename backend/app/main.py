from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import (
    auth,
    gardens,
    plots,
    sensor,
    advice,
    disease,
    chat,
    dashboard,
    devices,
    rules
)

# 创建数据库表
# Create database tables
Base.metadata.create_all(bind=engine)

# 初始化 FastAPI 应用
# Initialize FastAPI application
app = FastAPI(
    title="Tea Garden Brain API",
    description="Backend API for Tea Garden Management Platform",
    version="1.0.0"
)

# 配置 CORS 中间件，允许跨域请求
# Configure CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议限制域名 / Allow all origins, restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法 / Allow all HTTP methods
    allow_headers=["*"],  # 允许所有请求头 / Allow all headers
)

# 注册路由模块
# Register router modules
app.include_router(auth.router)        # 认证相关 / Authentication
app.include_router(dashboard.router)   # 仪表盘统计 / Dashboard statistics
app.include_router(gardens.router)     # 茶园管理 / Tea garden management
app.include_router(plots.router)       # 地块管理 / Plot management
app.include_router(devices.router)     # 设备管理 / Device management
app.include_router(sensor.router)      # 传感器数据 / Sensor data
app.include_router(advice.router)      # 农事建议 / Farming advice
app.include_router(disease.router)     # 病虫害识别 / Disease detection
app.include_router(chat.router)        # 智能问答 / AI Chat
app.include_router(rules.router)       # 规则引擎 / Rule engine

@app.get("/")
def root():
    """
    根路径测试接口
    Root endpoint for testing
    """
    return {"message": "Welcome to Tea Brain API"}
