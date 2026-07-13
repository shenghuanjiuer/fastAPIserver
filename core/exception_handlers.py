# core/exception_handlers.py

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from core.exceptions import BizException


async def biz_exception_handler(request: Request, exc: BizException):
    """捕获所有业务异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """改写 422 校验错误格式"""
    # exc.errors() 返回校验错误列表
    errors = exc.errors()
    # 取第一个错误简化提示
    first_error = errors[0] if errors else {}
    
    return JSONResponse(
        status_code=422,
        content={
            "code": 400,
            "message": f"参数校验失败: {first_error.get('msg', '未知错误')}",
            "data": {"errors": errors}
        }
    )