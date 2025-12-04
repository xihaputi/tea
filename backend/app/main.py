from fastapi import FastAPI # FastAPI 框架
from fastapi.middleware.cors import CORSMiddleware # 用于处理跨域请求
from contextlib import asynccontextmanager  # 用于生命周期管理
import asyncio # Import asyncio
from .mqtt_client import start_mqtt_loop, stop_mqtt_loop  # 如果你有关闭逻辑
# from .dev_processes import start_dev_dependencies  # 如果你要在开发环境自动拉起 emqx / node-red
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
    devices,
    rules,
    emqx
)

# 创建数据库表
# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ====== startup 阶段 ======
    # 1. 启动 MQTT 客户端（连接 EMQX 并订阅）
    start_mqtt_loop()

    # 启动设备状态检查任务
    import asyncio
    task = asyncio.create_task(check_device_status_loop())

    # 2. 开发环境：启动 EMQX 和 Node-RED（可选）
    #    正式环境一般不建议在这里启动外部服务，而是用系统服务来管理
    # start_dev_dependencies()  # 如果你不需要，可以删掉这一行

    # 把控制权交还给 FastAPI，开始处理请求
    yield

    # ====== shutdown 阶段 ======
    # 取消后台任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    # 如果你有 MQTT 或其他资源需要释放，在这里处理
    stop_mqtt_loop()  # 如果暂时没有关闭逻辑，可以先留空实现

async def check_device_status_loop():
    """后台任务：定期检查设备状态"""
    while True:
        try:
            check_device_status()
        except Exception as e:
            print(f"Error checking device status: {e}")
        await asyncio.sleep(60) # 每60秒检查一次

def check_device_status():
    """检查设备是否离线"""
    from app.database import SessionLocal
    from app.models import Device
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    try:
        # 查找状态为 online 但超过 5 分钟未更新的设备
        # Find devices that are online but haven't updated for > 5 mins
        threshold = datetime.utcnow() - timedelta(minutes=5)
        offline_devices = db.query(Device).filter(
            Device.status == "online",
            Device.last_time < threshold
        ).all()
        
        for device in offline_devices:
            print(f"Device {device.sn} is offline (timeout)")
            device.status = "offline"
        
        if offline_devices:
            db.commit()
    finally:
        db.close()

# 初始化 FastAPI 应用
# Initialize FastAPI application
app = FastAPI(
    title="Tea Garden Brain API",
    description="Backend API for Tea Garden Management Platform",
    version="1.0.0", 
    lifespan=lifespan
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
app.include_router(chat.router)        # 智能问答 / AI Chat
app.include_router(rules.router)       # 规则引擎 / Rule engine
app.include_router(emqx.router)        # EMQX 认证 / EMQX Auth
from .routers import alarms
app.include_router(alarms.router)      # 告警管理 / Alarm management
from .routers import users
app.include_router(users.router)       # 用户管理 / User management
from .routers import dashboard
app.include_router(dashboard.router)   # 仪表盘 / Dashboard

@app.get("/")
def root():
    """
    根路径测试接口
    Root endpoint for testing
    """
    return {"message": "Welcome to Tea Brain API"}
# Trigger reload for user management

