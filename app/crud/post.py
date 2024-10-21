from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Post
from app.schemas import PostResponse, PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    # Declare model specific CRUD operation methods.

    def get_all_from_author(self, db: Session, user_id: str) -> Post:
        return db.query(Post).filter(Post.author.id == user_id).first()

post = CRUDPost(Post)
