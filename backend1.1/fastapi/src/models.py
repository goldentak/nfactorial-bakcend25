from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "backendhw"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)