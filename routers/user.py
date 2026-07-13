# routers/user.py

from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    获取当前用户信息（需要认证）
    - 使用 Depends(get_current_user) 自动从 Token 解析用户
    """
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"]
    }


@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    """用户个人资料（需要认证）"""
    return {
        "message": f"欢迎回来，{current_user['username']}！",
        "user": current_user
    }