from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = "not_started"
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):

    id: int

    created_at: Optional[datetime]

    completed_at: Optional[datetime]

    due_date: Optional[datetime]

    class Config:
        from_attributes = True
class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: Optional[datetime] = None