from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Post
from app.schemas import PostResponse, PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    # Declare model specific CRUD operation methods.

    def get_one_by_filename(self, db: Session, filename: str) -> Post:
        return db.query(Post).filter(Post.filename == filename).first()


post = CRUDPost(Post)
