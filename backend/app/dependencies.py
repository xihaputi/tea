from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

def get_current_user(token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)) -> User:
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

def check_super_admin(user: User = Depends(get_current_user)):
    """
    检查是否为超级管理员
    Check if user is Super Admin
    """
    roles = user.roles.split(",") if user.roles else []
    if "admin" in roles and user.username == "admin": # 简单判断，实际应更严谨
        # 修正: 上面逻辑有漏洞，假设 'admin' 角色即为超级管理员? 
        # 用户需求明确: 1.超级管理员(all) 2.普通管理员(manage assigned) 3.普通用户(read assigned)
        # 我们可以约定 'super_admin' 角色，或者依然沿用 'admin' 但区分 check 逻辑
        # 现有 auth.py 初始化默认 admin 角色为 'admin'。
        # 我们可以保留 'admin' 作为超级管理员角色对于系统全局，或者引入 'super_admin'。
        # 鉴于现有数据可能只有 'admin'，我们暂时认为 'admin' + username='admin' 或者 角色包含 'super_admin' 为超级管理员。
        # 为了兼容性，如果没有 'super_admin' 角色，我们假设拥有 'admin' 且 id=1 是超级管理员?
        pass
    
    # 重新定义角色逻辑:
    # super_admin: 拥有所有权限. Role string contains 'super_admin' OR user is the seed admin.
    # admin: 普通管理员. Role string contains 'admin'.
    # user: 普通用户. Role string contains 'user'.
    
    if is_super_admin(user):
        return user
    
    raise HTTPException(status_code=403, detail="权限不足: 需要超级管理员权限")

def is_super_admin(user: User) -> bool:
    roles = user.roles.split(",") if user.roles else []
    return "super_admin" in roles or (user.username == "admin" and "admin" in roles)

def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    return user

def verify_garden_access(garden_id: int, user: User, require_manage: bool = False):
    """
    验证茶园访问权限
    Verify garden access permission
    """
    if is_super_admin(user):
        return True
    
    # 检查是否分配了该茶园
    # Check if garden is assigned
    assigned_garden_ids = [g.id for g in user.gardens]
    if garden_id not in assigned_garden_ids:
        raise HTTPException(status_code=403, detail=f"权限不足: 您未被分配管理茶园 ID {garden_id}")
    
    if require_manage:
        # 只有管理员(admin)角色可以管理(修改/删除/新建设备)
        roles = user.roles.split(",") if user.roles else []
        if "admin" not in roles:
             raise HTTPException(status_code=403, detail="权限不足: 您只有查看权限，无管理权限")
    
    return True
