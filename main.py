from fastapi import FastAPI
from database.database import Base, engine
from database import models  # 先导入模型，让 SQLAlchemy 注册到 Base.metadata
from routers.student import router as student_router

# 在所有模型导入后再创建表
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(student_router)
