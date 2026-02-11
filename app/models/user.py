from sqlalchemy import Column, String, Boolean,Integer
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index = True)
    name = Column(String(100), nullable = False)
    age = Column(Integer,nullable=False)
    is_vip = Column(Boolean, default=False)
