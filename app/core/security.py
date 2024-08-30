from typing import Optional, Dict, List
from datetime import datetime, timedelta

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.utils import first_party_caveats_parser

pwd_cxt = CryptContext(schemes="bcrypt", deprecated="auto")


# --------------------------------------------------------------------------
# PASSWORD HASHING METHODS
# --------------------------------------------------------------------------


def hash_password(plain_password: str):
    return pwd_cxt.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_cxt.verify(plain_password, hashed_password)


# --------------------------------------------------------------------------
# JWT TOKEN METHODS
# --------------------------------------------------------------------------


def create_jwt_access_token(
    sub: int, expires_delta_seconds: Optional[int] = None
) -> str:

    # Check if there is an expiration time given. If not use the default
    if expires_delta_seconds:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta_seconds)
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Prepare JWT token
    payload = {"exp": expire, "iat": datetime.utcnow(), "sub": str(sub)}
    encoded_jwt = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_SIGN_ALGORITHM
    )
    return encoded_jwt
