from typing import Generator
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from app.core import settings, OAuth2PasswordBearerWithCookie
from app.database.session import SessionLocal
from app import crud, models

from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

# *******************************************************************************
# SESSION DATABASE DEPENDENCY
# *******************************************************************************


def get_db() -> Generator:
    # Create session while connection to database
    try:
        db = SessionLocal()
        yield db
    # Once finish close database session
    finally:
        db.close()


# *******************************************************************************
# AUTHENTICATION DEPENDENCY
# *******************************************************************************

def get_current_user(
    access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:

    # Create HTTP Exception for credentilas error
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = None

    # Verify Access Token. If error found in verification, raise credentials exception
    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_SIGN_ALGORITHM]
        )
        user_id = payload.get("sub")

        # If no username id raise credentials exception (one passed as argument)
        if user_id is None:
            raise credentials_exception
        user = crud.user.get_one(db, model_id=user_id)
        return user

    # If error found during decoding JWT (mismatch in signature), raise credentials
    # exception (one passed as argument)
    except JWTError:
        raise credentials_exception
