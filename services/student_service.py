# Service 层 业务逻辑、调用数据库操作 直接接收 db: Session 参数

from typing import List, Optional
from schemas.student import Student
from database.models import Student as StudentModel

from sqlalchemy.orm import Session
from sqlalchemy import select
from database.database import add_data
from fastapi import UploadFile

class StudentService:

    @staticmethod
    def get_all_students(db:Session) :
        # select(StudentModel)数据库返回的是：Student对象。 select(Student)是生成SQL语句的函数
        # db.scalars()意思就是：返回对象集合。
        # .all()变成：list
        # scalar()返回一个对象。scalars()返回多个对象
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
    def update_student(id: int, student: Student,db:Session) -> Optional[StudentModel]:
        db_student = db.get(StudentModel,id)
        if db_student:
            for key,value in student.model_dump().items():
                setattr(db_student,key,value)
            db.commit()
            db.refresh(db_student)
            return db_student
        return None

    @staticmethod
    def partial_update(id: int, payload: dict, db: Session):
        obj = db.get(StudentModel, id)
        if not obj:
            return None
        for k, v in payload.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete_student(id: int, db:Session) -> bool:
        student = db.get(StudentModel,id)
        if student:
            db.delete(student)
            db.commit()
            return True
        return False

    @staticmethod
    def div_page(limit: int, offset: int, db:Session) -> List[StudentModel]:
        return db.scalars(select(StudentModel).offset(offset).limit(limit)).all()
    
    @staticmethod
    def up_load_file(file: UploadFile, db:Session) -> str:
        return file.filename

    @staticmethod
    def login_form(form: dict, db:Session) -> dict:
        return form
    