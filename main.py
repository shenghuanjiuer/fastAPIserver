from fastapi import FastAPI
from database.database import Base, engine
from database import models  # 先导入模型，让 SQLAlchemy 注册到 Base.metadata
from routers.student import router as student_router
from fastapi.exceptions import RequestValidationError
from core.exceptions import BizException
from core.exception_handlers import biz_exception_handler, validation_exception_handler
from routers.auth import router as auth_router
from routers.user import router as user_router

# 在所有模型导入后再创建表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 注册异常处理器（必须在路由注册之前）
app.add_exception_handler(BizException, biz_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(student_router)
app.include_router(auth_router)  # 认证路由
app.include_router(user_router)  # 用户路由
