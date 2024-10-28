from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.api.deps import get_db, get_current_user, admin_only

router = APIRouter()


@router.get("", response_model=List[schemas.UserResponse])
def read_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> list[models.User]:
    """
    Retrieve all users.
    """
    users = crud.user.get_all(db)
    return users


@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve current user logged in.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_one_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Retrieve one user by id.

    **Path Parameters:**

        - user_id: ID of the user.

    **Returns:**

        - id: ID of the user.
        - username: Username of the user.
        - email: Email of the user.
        - comment:
            - id: ID of the comment.
            - name: Name of the comment.
            - type: Type of the comment.

    **Raises:**

        - 404 (Not Found): User with the specified ID does not exist.
        - 422 (Unprocessable Entity): Invalid data arguments provided in the request.
    """

    user = crud.user.get_one(db, model_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id '{user_id}' does not exist in the system.",
        )
    return user


@router.post("", response_model=schemas.UserResponse)
def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate, current_user: models.User = Depends(admin_only)) -> Any:
    """
    Create new user.
    """
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(*, user_id: int, db: Session = Depends(get_db), user_in: schemas.UserUpdate, current_user: models.User = Depends(admin_only)) -> Any:
    """
    Update existing user.
    """
    user = crud.user.get_one(db, model_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id '{user_id}' does not exist in the system.",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("", response_model=schemas.Message)
def delete_all_users(*, db: Session = Depends(get_db), current_user: models.User = Depends(admin_only)) -> dict[str, str]:
    """
    Delete all users.
    """
    users = crud.user.get_all(db)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"It doesn't exist any user in the system.",
        )
    rows_deleted = crud.user.remove_all(db)
    return {"message": f"{rows_deleted} users were deleted."}


@router.delete("/{user_id}", response_model=schemas.Message)
def delete_one_user(*, user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(admin_only)) -> dict[str, str]:
    """
    Delete one user by id.
    """
    user = crud.user.get_one(db, model_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id {user_id} does not exist in the system.",
        )
    crud.user.remove_one(db, model_id=user.id)
    return {"message": f"User with ID = '{user_id}' deleted."}
