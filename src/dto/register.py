from pydantic import BaseModel, field_validator
from datetime import date, datetime

from src.utils import get_hashed_password
from humps import camelize

def to_camel(string):
    return camelize(string)

class CamelModel(BaseModel):
    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }

class Register(CamelModel):
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


class Login(CamelModel):
    email: str
    password: str

class Login2FA(CamelModel):
    email: str
    totp: str


class TokenSchema(CamelModel):
    access_token: str
    refresh_token: str


class Enable2FAResponse(CamelModel):
    message: str


class RefreshToken(CamelModel):
    refresh_token: str


class TOTP(CamelModel):
    totp: str


class RegisterResponse(CamelModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: datetime
    phone: str