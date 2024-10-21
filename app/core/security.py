from typing import Optional, Dict
from datetime import datetime, timedelta
from urllib.parse import unquote

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

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

# --------------------------------------------------------------------------
# OAUTH2 SCHEMES
# --------------------------------------------------------------------------

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[dict]:

        authorization: str = request.cookies.get(
            "access_token"
        )  # changed to accept access token from httpOnly Cookie

        if authorization is not None:
            authorization = unquote(authorization)

        scheme, access_token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return access_token
