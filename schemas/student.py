from typing import Optional,List
from pydantic import BaseModel,Field,EmailStr


class Student(BaseModel):
    name: str = Field(
        min_length=2,max_length=20,
        description="学生姓名",
        example = "张三"
        )
    age: int = Field(ge=0,le=120)
    city: str = "Beijing"
    # email:Optional[EmailStr] = None

   