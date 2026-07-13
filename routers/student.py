# 路由层 使用 Depends(get_db)

from typing import List
from fastapi import APIRouter, status, Depends, Path, Query, Body
from schemas.student import Student, StudentOut, ResponseModel, StudentUpdate
from services.student_service import StudentService
from core.exceptions import NotFoundException
from dependencies.pagination import Pagination
from dependencies import DBSession

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=ResponseModel[List[StudentOut]])
def get_students(db: DBSession, pagination: Pagination = Depends()):
    students = StudentService.get_all_students(db, pagination)
    return ResponseModel(data=students)


@router.get("/search")
def get_students(
    db: DBSession,
    name: str = Query(..., description="学生姓名", min_length=2)
):
    return StudentService.get_student_by_name(name, db)


@router.get("/city/{city}")
def get_students_by_city(
    db: DBSession,
    city: str = Path(..., description="城市名称")
):
    return StudentService.get_students_by_city(city, db)


@router.get("/{student_id}", response_model=ResponseModel[StudentOut])
def get_student(
    db: DBSession,
    student_id: int = Path(..., description="学生ID")
):
    obj = StudentService.get_student_by_id(student_id, db)
    if not obj:
        raise NotFoundException(message="学生不存在")
    return ResponseModel(data=obj)


@router.post("", response_model=ResponseModel[StudentOut], status_code=status.HTTP_201_CREATED)
def create_student(
    db: DBSession,
    student: Student = Body(..., description="学生信息")
):
    new_obj = StudentService.create_student(student, db)
    return ResponseModel(data=new_obj)


@router.put("/{id}", response_model=ResponseModel[StudentOut], status_code=status.HTTP_201_CREATED)
def update_student(
    db: DBSession,
    id: int = Path(..., description="学生ID"),
    student: Student = Body(..., description="学生信息")
):
    updated_obj = StudentService.update_student(id, student, db)
    if not updated_obj:
        raise NotFoundException(message="学生不存在")
    return ResponseModel(data=updated_obj)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    db: DBSession,
    id: int = Path(..., description="学生ID")
):
    ok = StudentService.delete_student(id, db)
    if not ok:
        raise NotFoundException(message="学生不存在")
    return None


@router.patch(
    "/{id}",
    response_model=ResponseModel[StudentOut],
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED
)
def patch_student(
    db: DBSession,
    id: int = Path(..., description="学生ID"),
    student: StudentUpdate = Body(..., description="学生信息")
):
    payload = student.model_dump(exclude_unset=True)
    updated = StudentService.partial_update(id, payload, db)
    if not updated:
        raise NotFoundException(message="学生不存在")
    return ResponseModel(data=updated)