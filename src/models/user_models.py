from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Boolean
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True, default='')
    last_name: Mapped[str] = mapped_column(String(50), nullable=True, default='')
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    two_factor_auth: Mapped[bool] = mapped_column(Boolean, nullable=True)
    totp_secret: Mapped[str] = mapped_column(String, nullable=True)