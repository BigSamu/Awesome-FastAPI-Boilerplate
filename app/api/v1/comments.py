from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_db, get_current_user


router = APIRouter()


@router.get("", response_model=List[schemas.CommentResponse])
def read_all_comments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve all comments.
    """
    comments = crud.comment.get_all(db)
    return comments

@router.get("/{comment_id}", response_model=schemas.CommentResponse)
def read_one_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve one comment by id.
    """
    comment = crud.comment.get_one(db, model_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The comment with id '{comment_id}' does not exist in the database.",
        )
    return comment

@router.post("", response_model=schemas.CommentResponse)
def create_comment(*, db: Session = Depends(get_db), comment_in: schemas.CommentCreate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Create new comment.
    """
    comment =  crud.comment.get_one_by_name(db,name=comment_in.name)
    if comment:
          raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Comment already exist in database.",
        )
    comment = crud.comment.create(db, obj_in=comment_in)

    return comment

@router.put("/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(*, comment_id: int, db: Session = Depends(get_db), comment_in: schemas.CommentUpdate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Update one comment by id.
    """
    comment = crud.comment.get_one(db, model_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The comment with id '{comment_id}' does not exist in the database.",
        )
    comment = crud.comment.update(db, db_obj=comment, obj_in=comment_in)

    return comment

@router.delete("", response_model=schemas.Message)
def delete_all_comments(*, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete all comments.
    """
    comments = crud.comment.get_all(db)
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"It doesn't exist any comment in the database.",
        )
    rows_deleted = crud.comment.remove_all(db)
    return {"message": f"{rows_deleted} comments were deleted."}

@router.delete("/{comment_id}", response_model=schemas.Message)
def delete_one_comment(*, comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete one comment by id.
    """
    comment = crud.comment.get_one(db, model_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The comment with id '{comment_id}' does not exist in the database.",
        )
    crud.comment.remove_one(db, model_id=comment.id)
    return {"message": f"The comment with id '{comment_id}' deleted."}
