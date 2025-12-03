import uuid
import base64
import io
import random
from typing import Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Body, Header
from sqlalchemy.orm import Session
from captcha.image import ImageCaptcha

from ..database import get_db
from ..models import User
from ..schemas import LoginRequest, LoginResponse, UserInfo

router = APIRouter(prefix="/auth", tags=["auth"])

# 简单的内存缓存存储验证码，实际生产应使用 Redis
# Simple in-memory cache for storing captchas, use Redis in production
# Key: captcha_key, Value: { "code": "1234", "expire": datetime }
CAPTCHA_STORE = {}

def clean_expired_captcha():
    """
    清理过期验证码
    Clean up expired captchas
    """
    now = datetime.now()
    expired_keys = [k for k, v in CAPTCHA_STORE.items() if v["expire"] < now]
    for k in expired_keys:
        del CAPTCHA_STORE[k]

@router.get("/captcha")
def get_captcha():
    """
    获取图形验证码
    Get image captcha
    """
    clean_expired_captcha()
    
    # 生成 4 位数字验证码
    # Generate 4-digit numeric captcha
    image = ImageCaptcha(width=100, height=40)
    code = "".join(random.choices("0123456789", k=4))
    data = image.generate(code)
    
    # 转为 Base64
    # Convert to Base64
    b64_img = base64.b64encode(data.read()).decode("utf-8")
    
    # 生成唯一 Key 并存储
    # Generate unique Key and store
    key = str(uuid.uuid4())
    CAPTCHA_STORE[key] = {
        "code": code,
        "expire": datetime.now() + timedelta(minutes=5)
    }
    
    return {"key": key, "image": f"data:image/png;base64,{b64_img}"}

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录接口（已去除验证码，固定账号 admin/admin 可用）
    """
    # 初始化默认管理员（admin/admin）
    if db.query(User).count() == 0:
        default_admin = User(
            username="admin",
            password="admin",
            name="超级管理员",
            avatar="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
            roles="admin",
        )
        db.add(default_admin)
        db.commit()
        db.refresh(default_admin)

    user = db.query(User).filter(User.username == payload.username).first()
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="账号或密码错误")

    user_info = UserInfo(
        id=user.id,
        name=user.name,
        avatar=user.avatar or "",
        roles=user.roles.split(",") if user.roles else [],
    )
    return LoginResponse(token=f"token-{user.id}-{user.username}", userInfo=user_info)

@router.post("/register")
def register(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    name: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    User registration endpoint
    """
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
        
    new_user = User(
        username=username,
        password=password,
        name=name,
        roles="user" # 默认普通用户 / Default to normal user
    )
    db.add(new_user)
    db.commit()
    return {"success": True, "msg": "注册成功"}

@router.post("/reset-password")
def reset_password(
    username: str = Body(..., embed=True),
    newPassword: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    重置密码接口
    Reset password endpoint
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
        
    user.password = newPassword
    db.commit()
    return {"success": True, "msg": "密码重置成功"}

def get_current_user(token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)):
    """
    获取当前用户的依赖函数
    Dependency to get current user
    """
    # 允许 Authorization: Bearer token-xxx
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    if not token.startswith("token-"):
        raise HTTPException(status_code=401, detail="无效的 Token")
    
    try:
        parts = token.split("-")
        if len(parts) < 3:
             raise HTTPException(status_code=401, detail="无效的 Token 格式")
        user_id = int(parts[1])
    except:
        raise HTTPException(status_code=401, detail="Token 解析失败")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

@router.get("/user/info", response_model=UserInfo)
def user_info(user: User = Depends(get_current_user)):
    """
    获取用户信息接口
    Get user info endpoint
    """
    return UserInfo(
        id=user.id,
        name=user.name,
        avatar=user.avatar or "",
        roles=user.roles.split(",") if user.roles else []
    )

@router.post("/logout")
def logout():
    """
    退出登录接口
    Logout endpoint
    """
    return {"success": True}
