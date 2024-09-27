from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone
from typing import Union, Any, Annotated
from jose import jwt
from fastapi import HTTPException, status, Depends
from configurations.app_config import settings
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import pyotp

from src.models.user_models import User

from sqlalchemy.orm import Session


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Refresh token expired, please login to get new token!"
    except jwt.JWTError:
        raise "Invalid refresh token."

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scheme_name="JWT"
)

class TokenData(BaseModel):
    email: str | None = None

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(settings.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token provided",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.JWTError:
        raise credentials_exception
    print("email before filtering the user: ", email)
    user = db.query(User).filter(token_data.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def generate_qr_code(totp_secret):
    totp = pyotp.TOTP(totp_secret)
    provisioning_uri = totp.provisioning_uri(name='Raheel', issuer_name='Microsoft Authenticator')
    return provisioning_uri

def verify_secret(user_sec, totp_code):
    totp = pyotp.TOTP(user_sec.strip())
    generated_code = totp.now()
    print("generated code: ", generated_code)
    if totp.verify(totp_code.strip(), valid_window=1):
        print("inside true")
        return True
    return None