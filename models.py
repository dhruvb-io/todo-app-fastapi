from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base

class TodoModel(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text, index=True, nullable=True) # Changed from String to Text
    completed = Column(Boolean, default=False)