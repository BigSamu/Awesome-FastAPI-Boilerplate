from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Comment
from app.schemas import CommentResponse, CommentCreate, CommentUpdate

class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    # Declare model specific CRUD operation methods.

    def get_all_from_post(self, db: Session, post_id: str) -> Comment:
        return db.query(Comment).filter(Comment.post.id == post_id).first()

    def get_all_from_commenter(self, db: Session, user_id: str) -> Comment:
        return db.query(Comment).filter(Comment.commenter.id == user_id).first()


comment = CRUDComment(Comment)
