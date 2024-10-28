from typing import Dict

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session

from app import schemas, crud, models
from app.core import (
    create_jwt_access_token,
)
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/login", response_model=schemas.UserResponse)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    authenticated_user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Create JWT token
    access_token = create_jwt_access_token(sub=authenticated_user.id)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=86400000,
        httponly=True,
        samesite="strict",
    )

    # Return access token
    return authenticated_user


@router.post("/register", response_model=schemas.UserResponse)
def register(
    response: Response,
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    user = crud.user.get_one_by_email(db, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    registered_user = crud.user.create(db, obj_in=user_in)

    # Create JWT token
    access_token = create_jwt_access_token(sub=registered_user.id)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=86400000,
        httponly=True,
        samesite="strict",
    )

    return registered_user

@router.get("/logout", response_model=schemas.Message)
def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True)
    return {"message": "Succesfully Log Out"}
