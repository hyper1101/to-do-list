from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    created_at: datetime
    due_date: datetime | None = None

class TodoCreate(TodoBase):
    pass

class TodoOut(TodoBase):
    id: int
    completed: bool
    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class TodoStats(BaseModel):
    total: int
    completed: int
    pending: int
    overdue: int
