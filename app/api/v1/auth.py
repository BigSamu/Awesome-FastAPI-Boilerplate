from typing import Dict

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from sqlalchemy.orm.session import Session

from app import schemas, crud
from app.core import (
    create_jwt_access_token,
)
from app.api.deps import get_db

router = APIRouter()

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_authenticated = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )

    if not user_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Create JWT token
    access_token = create_jwt_access_token(sub=user_authenticated.id)

    # Return access token
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout")
def logout():
    return {"message": "Succesfully Log Out"}
