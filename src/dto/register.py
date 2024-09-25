from pydantic import BaseModel, field_validator
from datetime import date

from src.utils import get_hashed_password


class Register(BaseModel):
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    date_of_birth: date | None = None
    two_factor_auth: bool | None = False

    @property
    def date_of_birth_str(self):
        return self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None

    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, value):  # build in type email : https://stackoverflow.com/questions/76972389/fastapi-pydantic-how-to-validate-email
        if '@' not in value:
            raise ValueError('Invalid email format')
        return value

    @field_validator('password')
    @classmethod
    def password_strength(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return get_hashed_password(value)

class Login(BaseModel):
    email: str
    password: str

class Login2FA(BaseModel):
    email: str
    totp: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class Enable2FAResponse(BaseModel):
    message: str

class RefreshToken(BaseModel):
    refresh_token: str

class TOTP(BaseModel):
    totp: str