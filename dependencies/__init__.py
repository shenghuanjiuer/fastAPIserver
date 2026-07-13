from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.database import get_current_student

# 预定义常用依赖类型
DBSession = Annotated[Session, Depends(get_db)]
CurrentStudent = Annotated[dict, Depends(get_current_student)]
