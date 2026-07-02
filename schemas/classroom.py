from .student import Student
from pydantic import BaseModel
from typing import List

class Classrom(BaseModel):
    students:List[Student]