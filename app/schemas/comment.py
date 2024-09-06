from pydantic import BaseModel
from app.schemas import UserResponse, PostResponse

class CommentCreate(BaseModel):
    comment: str
    commenter_id: int
    post_id: int

class CommentUpdate(BaseModel):
    name: str | None
    commenter_id: int | None
    post_id: int | None

class CommentResponse(BaseModel):
    id: int
    name: str
    type: str
    commenter: UserResponse
    post: PostResponse

    class Config:
        from_attributes = True
