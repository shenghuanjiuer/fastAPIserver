from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column
from database.database import Base

class Student(Base):
    __tablename__ = "students"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True
    )

    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)
    city:Mapped[str] = mapped_column(String)