from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from database.database import Base

class Student(Base):
    __tablename__ = "students"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True
    )
    classroom_id :Mapped[int] = mapped_column(
        ForeignKey("classrooms.id") # 这一列的数据必须来自 classrooms 表中的 id 字段。
    )
    # 映射到数据库字符串字段，Python 侧取值类型是 str 。 mapped_column(String)定义真实数据库列,String：数据库字段类型
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)
    city:Mapped[str] = mapped_column(String)

    # relationship() 负责让 Python 能够方便地访问关系。
    # （只存在 Python 对象里，不会在数据库生成新列，外键要单独用 ForeignKey 写在本表）
    classroom:Mapped["Classroom"] = relationship(  
        "Classroom",
        back_populates="students"
    )
    


class Classroom(Base):
    __tablename__ = "classrooms"

    id :Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True
    )
    class_name :Mapped[str] = mapped_column(String)

    students :Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="classroom"
    )

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="user")  # user/admin
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)