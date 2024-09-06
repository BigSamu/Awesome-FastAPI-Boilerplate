from typing import Optional

from pydantic import BaseModel

class CommentCreate(BaseModel):
    name: str
    type: str

class CommentUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]

class CommentResponse(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True
