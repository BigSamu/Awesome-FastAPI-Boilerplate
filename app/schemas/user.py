from enum import Enum
from pydantic import BaseModel, EmailStr

class Role(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None
    email: str | None
    password: str | None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: list[int] = []
    comments: list[int] = []

    class Config:
        from_attributes = True
