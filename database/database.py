from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,Session



DATABASE_URL = "sqlite:///student.db"

# 创建数据库引擎
# echo = True 用于打印数据库语句
# 可以根据需要关闭
engine = create_engine(
    DATABASE_URL,
    echo = True
)

SessionLocal = sessionmaker(
    bind = engine
)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)

# 查询数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 在数据库新增数据
def add_data(db:Session, data:Base):
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        db.rollback()
        raise e
