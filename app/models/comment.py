from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(255), nullable=False)
    commenter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))

    post = relationship("Post", back_populates="comments")
    commenter = relationship("User", back_populates="comments")

    def __repr__(self):
         return ("<Comment {self.id}, post_title: {self.post.title}, commenter: {self.commenter.username}>").format(self=self)
