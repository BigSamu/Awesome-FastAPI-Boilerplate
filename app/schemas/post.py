
from app.schemas import UserResponse
from pydantic import BaseModel

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

    class Config:
        from_attributes = True
