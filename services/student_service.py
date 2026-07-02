from typing import List, Optional

from sqlalchemy.orm.base import PASSIVE_OFF
from schemas.student import Student
from database.models import Student as StudentModel
from database.data import students
from fastapi import Depends
from dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.database import get_db,add_data

class StudentService:

    @staticmethod
    def get_all_students(db:Session) :
        return db.scalars(select(StudentModel)).all()

    @staticmethod
    def get_student_by_id(student_id:int,db:Session) -> Optional[StudentModel]:
        return db.get(StudentModel,student_id)  # get 只能查主键

    @staticmethod
    def get_student_by_name(name: str,db:Session) -> Optional[StudentModel]:
        # .first()：取匹配到的第一条，无数据返回 None
        return db.scalars(select(StudentModel).where(StudentModel.name == name)).first()

    @staticmethod
    def get_students_by_city(city: str,db:Session) -> List[StudentModel]:
        return db.scalars(select(StudentModel).where(StudentModel.city == city)).all()

    @staticmethod
    def create_student(student: Student,db:Session) -> StudentModel:
        new_student = StudentModel(**student.model_dump())
        return add_data(db, new_student)

    @staticmethod
    def update_student(id: int, student: Student) -> Optional[dict]:
        for s in students:
            if s["id"] == id:
                s.update(student.model_dump())
                return s
        return None

    @staticmethod
    def delete_student(id: int) -> bool:
        for index, student in enumerate(students):
            if student["id"] == id:
                students.pop(index)
                return True
        return False
    
    @staticmethod
    def me(user = Depends(get_current_user)):
        return user