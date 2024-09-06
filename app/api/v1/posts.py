from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.api.deps import get_db, get_current_user


router = APIRouter()

@router.get("", response_model=List[schemas.PostResponse])
def read_all_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve all posts.
    """
    posts = crud.post.get_all(db)
    return posts

@router.get("/{post_id}", response_model=schemas.PostResponse)
def read_one_post(post_id:int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve one post by id.
    """
    post = crud.post.get_one(db, model_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id '{post_id}' does not exist in the system.",
        )
    return post

@router.post("", response_model=schemas.PostResponse)
def create_post(*, db: Session = Depends(get_db), post_in: schemas.PostCreate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Create new post.
    """
    post = crud.post.create(db, obj_in=post_in)
    return post

@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(*, post_id: int, db: Session = Depends(get_db), post_in: schemas.PostUpdate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Update existing post.
    """
    post = crud.post.get_one(db, model_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id '{post_id}' does not exist in the system.",
        )
    post = crud.post.update(db, db_obj=post, obj_in=post_in)
    return post

@router.delete("", response_model=schemas.Message)
def delete_all_posts(*, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete all posts.
    """
    posts = crud.post.get_all(db)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"It doesn't exist any post in the system.",
        )
    rows_deleted=crud.post.remove_all(db)
    return {"message": f"{rows_deleted} posts were deleted."}


@router.delete("/{post_id}", response_model=schemas.Message)
def delete_one_post(*, post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete one post by id.
    """
    post = crud.post.get_one(db, model_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id '{post_id}' does not exist in the system.",
        )
    crud.post.remove_one(db, model_id=post.id)
    return {"message": f"Post with id '{post_id}' deleted."}
