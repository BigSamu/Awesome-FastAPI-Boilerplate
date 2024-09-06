from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas import CommentResponse


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    comment_id: int


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    comment_id: Optional[int]


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    comment: CommentResponse

    class Config:
        from_attributes = True
