import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, TeaGarden
from ..schemas import UserCreate, UserUpdate, UserOut, UserPageResult

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserPageResult)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    keyword: str = "",
    db: Session = Depends(get_db)
):
    """
    获取用户列表
    Get user list
    """
    try:
        query = db.query(User)
        if keyword:
            query = query.filter(User.name.contains(keyword) | User.username.contains(keyword))
            
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        
        # 手动处理 permissions 和 garden_ids
        result = []
        for item in items:
            perms = []
            try:
                if item.permissions:
                    loaded = json.loads(item.permissions)
                    if isinstance(loaded, list):
                        perms = loaded
            except Exception as e:
                print(f"Error parsing permissions for user {item.id}: {e}")
                
            out = UserOut(
                id=item.id,
                username=item.username,
                name=item.name,
                roles=item.roles.split(",") if item.roles else [],
                permissions=perms,
                garden_ids=[g.id for g in item.gardens]
            )
            result.append(out)
            
        return {"list": result, "total": total}
    except Exception as e:
        print(f"Error in list_users: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    创建用户
    Create user
    """
    # 检查用户名是否存在
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
        
    # 获取关联的茶园
    gardens = []
    if user_in.garden_ids:
        gardens = db.query(TeaGarden).filter(TeaGarden.id.in_(user_in.garden_ids)).all()
        
    new_user = User(
        username=user_in.username,
        password=user_in.password, # 实际应加密
        name=user_in.name,
        roles=",".join(user_in.roles),
        permissions=json.dumps(user_in.permissions),
        gardens=gardens
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserOut(
        id=new_user.id,
        username=new_user.username,
        name=new_user.name,
        roles=new_user.roles.split(",") if new_user.roles else [],
        permissions=json.loads(new_user.permissions) if new_user.permissions else [],
        garden_ids=[g.id for g in new_user.gardens]
    )


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    """
    更新用户
    Update user
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_in.password:
        user.password = user_in.password
    if user_in.name:
        user.name = user_in.name
    if user_in.roles is not None:
        user.roles = ",".join(user_in.roles)
    if user_in.permissions is not None:
        user.permissions = json.dumps(user_in.permissions)
    if user_in.garden_ids is not None:
        gardens = db.query(TeaGarden).filter(TeaGarden.id.in_(user_in.garden_ids)).all()
        user.gardens = gardens
        
    db.commit()
    db.refresh(user)
    
    return UserOut(
        id=user.id,
        username=user.username,
        name=user.name,
        roles=user.roles.split(",") if user.roles else [],
        permissions=json.loads(user.permissions) if user.permissions else [],
        garden_ids=[g.id for g in user.gardens]
    )


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    删除用户
    Delete user
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return {"success": True}
