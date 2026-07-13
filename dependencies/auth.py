# dependencies/auth.py (完整实现)

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# 从配置模块加载
from core.config import settings

# 使用配置
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# ===== 密码哈希 =====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===== OAuth2 认证 =====
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ===== 密码工具函数 =====
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


# ===== JWT 工具函数 =====
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建 JWT Token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """解码 JWT Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ===== 依赖注入函数 =====
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)  # 需要从 database 导入 get_db
) -> dict:
    """
    从 Token 中获取当前用户（依赖注入）
    使用方式: current_user: dict = Depends(get_current_user)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 解码 token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # 从数据库查询用户
    from database.models import User  # 避免循环导入
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }


def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """获取当前活跃用户（可添加额外检查）"""
    return current_user


def require_role(required_role: str):
    """
    角色权限依赖工厂函数
    使用方式: current_user: dict = Depends(require_role("admin"))
    """
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要 {required_role} 权限"
            )
        return current_user
    
    return role_checker


# 简化版：直接导出管理员依赖
require_admin = require_role("admin")