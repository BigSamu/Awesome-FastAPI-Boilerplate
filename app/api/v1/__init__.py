from fastapi import APIRouter

from app.api.v1 import posts, users, auth, comments

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
