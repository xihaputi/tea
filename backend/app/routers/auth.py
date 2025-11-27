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
# Key: captcha_key, Value: { "code": "1234", "expire": datetime }
CAPTCHA_STORE = {}

def clean_expired_captcha():
    """清理过期验证码"""
    now = datetime.now()
    expired_keys = [k for k, v in CAPTCHA_STORE.items() if v["expire"] < now]
    for k in expired_keys:
        del CAPTCHA_STORE[k]

@router.get("/captcha")
def get_captcha():
    clean_expired_captcha()
    
    # 生成 4 位数字验证码
    image = ImageCaptcha(width=100, height=40)
    code = "".join(random.choices("0123456789", k=4))
    data = image.generate(code)
    
    # 转为 Base64
    b64_img = base64.b64encode(data.read()).decode("utf-8")
    
    # 生成唯一 Key 并存储
    key = str(uuid.uuid4())
    CAPTCHA_STORE[key] = {
        "code": code,
        "expire": datetime.now() + timedelta(minutes=5)
    }
    
    return {"key": key, "image": f"data:image/png;base64,{b64_img}"}

@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest, 
    db: Session = Depends(get_db)
):
    # 1. 验证码校验
    if not payload.captchaKey or not payload.captchaCode:
         raise HTTPException(status_code=400, detail="请输入验证码")
    
    stored = CAPTCHA_STORE.get(payload.captchaKey)
    if not stored:
        raise HTTPException(status_code=400, detail="验证码已过期，请刷新")
    
    if stored["code"] != payload.captchaCode:
        raise HTTPException(status_code=400, detail="验证码错误")
        
    # 验证通过后删除
    del CAPTCHA_STORE[payload.captchaKey]

    # 2. 检查数据库是否有用户，自动初始化逻辑保留
    if db.query(User).count() == 0:
        default_admin = User(
            username="admin",
            password="123456",
            name="超级管理员",
            avatar="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
            roles="admin"
        )
        db.add(default_admin)
        db.commit()
        db.refresh(default_admin)
    
    # 3. 查库验证
    user = db.query(User).filter(User.username == payload.username).first()
    
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="账号或密码错误")
        
    user_info = UserInfo(
        id=user.id,
        name=user.name,
        avatar=user.avatar or "",
        roles=user.roles.split(",") if user.roles else []
    )
    return LoginResponse(token=f"token-{user.id}-{user.username}", userInfo=user_info)

@router.post("/register")
def register(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    name: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
        
    new_user = User(
        username=username,
        password=password,
        name=name,
        roles="user" # 默认普通用户
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
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
        
    user.password = newPassword
    db.commit()
    return {"success": True, "msg": "密码重置成功"}

def get_current_user(token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)):
    # 简单的 Token 解析: "token-{id}-{username}"
    # 注意：实际生产必须使用 JWT
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
    return UserInfo(
        id=user.id,
        name=user.name,
        avatar=user.avatar or "",
        roles=user.roles.split(",") if user.roles else []
    )

@router.post("/logout")
def logout():
    return {"success": True}
