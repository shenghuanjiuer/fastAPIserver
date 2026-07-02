# 路由层 使用 Depends(get_db)

from fastapi import APIRouter, HTTPException
from schemas.student import Student
from services.student_service import StudentService
from database.database import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/students", tags=["students"])


@router.get("")
def get_students(db: Session = Depends(get_db)):
    return StudentService.get_all_students(db)


@router.get("/search")
def get_students(name: str, db: Session = Depends(get_db)):
    return StudentService.get_student_by_name(name, db)
    


@router.get("/city/{city}")
def get_students_by_city(city: str):
    return StudentService.get_students_by_city(city)


@router.get("/{student_id}")
def get_student(student_id: int):
    student = StudentService.get_student_by_id(student_id)
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")


@router.post("")
def create_student(student: Student,db: Session = Depends(get_db)):
    return StudentService.create_student(student,db)


@router.put("/{id}")
def update_student(id: int, student: Student):
    result = StudentService.update_student(id, student)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/{id}")
def delete_student(id: int):
    if StudentService.delete_student(id):
        return {"message": "删除成功"}
    raise HTTPException(status_code=404, detail="Student not found")
