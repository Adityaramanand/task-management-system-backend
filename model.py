from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)

    email = Column(String, unique=True, index=True)

    password = Column(String)

    role = Column(String, default="user")  

    tasks = relationship("Task", back_populates="owner")


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String)

    priority = Column(String)

    status = Column(String, default="not_started")

    created_at = Column(DateTime, default=datetime.now)

    due_date  = Column(DateTime, nullable=True)

    completed_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")