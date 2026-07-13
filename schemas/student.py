from typing import Optional,List,Generic, TypeVar
from pydantic import BaseModel,Field,EmailStr,ConfigDict


class Student(BaseModel):
    name: str = Field(
        min_length=2,max_length=20,
        description="学生姓名",
        example = "张三"
        )
    age: int = Field(ge=0,le=120)
    city: str = "Beijing"
    # email:Optional[EmailStr] = None

class StudentOut(Student):
    model_config = ConfigDict(from_attributes=True)   # ★ 必加
    id: int
    # name/age/city 自动继承
    classroom_id : int


T = TypeVar("T")

class ResponseModel(BaseModel,Generic[T]):
    code: int = 0
    msg: str = "ok"
    data: Optional[T] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=20)
    age: Optional[int]   = Field(default=None, ge=0, le=120)
    city: Optional[str]  = None