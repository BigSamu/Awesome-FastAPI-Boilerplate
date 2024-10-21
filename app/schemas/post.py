from pydantic import BaseModel
from app.schemas.user import UserResponse

class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int

class PostUpdate(BaseModel):
    title: str | None
    body: str | None
    author_id: int | None

class PostResponse(BaseModel):
    title: str
    body: str
    author: UserResponse
    comments: list[int]

    class Config:
        from_attributes = True
