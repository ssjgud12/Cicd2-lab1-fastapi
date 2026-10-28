from sqlalchemy import Column, Integer, String
from app.database import Base

class UserDB(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, index=True) # MUST BE userid
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    student_id = Column(String, unique=True, index=True, nullable=False)