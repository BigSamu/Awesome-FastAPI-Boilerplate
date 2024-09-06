from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Comment
from app.schemas import CommentResponse, CommentCreate, CommentUpdate

class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    # Declare model specific CRUD operation methods.

    def get_one_by_name(self, db: Session, name: str) -> Comment:
        return db.query(Comment).filter(Comment.name == name).first()


comment = CRUDComment(Comment)
