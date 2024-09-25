import pyotp

from fastapi import FastAPI,  Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dto.register import Register, Login, TokenSchema, RefreshToken, TOTP, Login2FA, Enable2FAResponse
from configurations.app_config import settings

from src.models.user_models import User

import qrcode
import base64
from io import BytesIO

from fastapi import HTTPException, status, Depends

from src.utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_refresh_token,
    get_current_user,
    generate_qr_code,
    verify_secret
)

app = FastAPI()


@app.post('/api/v1/auth/register')
async def register(
    data: Register,
    db: Session = Depends(settings.get_db)
) -> Register:
    """
    Create new User
    """
    item = User(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.post('/api/v1/auth/login', summary="Create access and refresh tokens for user", response_model=TokenSchema | Enable2FAResponse)
async def login(
    data: Login,
    db: Session = Depends(settings.get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if user.two_factor_auth:
        return {
            "message": "Please enter 2fa code."
        }

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }

@app.post('/api/v1/auth/login-2fa/', summary="Login with 2FA", response_model=TokenSchema | Enable2FAResponse)
async def login_2fa(
    data: Login2FA,
    db: Session = Depends(settings.get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    user_secret = user.totp_secret
    if user_secret:
        verified = verify_secret(user_secret, data.totp)
        if verified:
            return {
                "access_token": create_access_token(user.email),
                "refresh_token": create_refresh_token(user.email),
            }
        else:
            return {
                "message": "Invalid totp, please try again!"
            }
    return {
        "message": "Please enable 2FA first!"
    }


@app.post('/api/v1/auth/refresh_token/')
async def refresh_token(
    data: RefreshToken,
    db: Session = Depends(settings.get_db)
):
    try:
        payload = verify_refresh_token(data.refresh_token)
        user_email = payload['sub']

        user = db.query(User).filter(User.email == user_email).first()
        if user is None:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        new_access_token = create_access_token(user.email)

        return {
            "access_token": new_access_token,
            "refresh_token": data.refresh_token
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    

@app.get('/api/v1/auth/enable-2fa')
async def refresh_token(
    db: Session = Depends(settings.get_db),
    user: User = Depends(get_current_user)
):
    totp_secret = pyotp.random_base32()
    uri = generate_qr_code(totp_secret)
    user = db.query(User).filter(User.email == user.email).first()
    user.totp_secret = totp_secret
    db.commit()

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    qr_image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return {
        "URI": uri,
        "QR_Code": f"data:image/png;base64,{qr_image_base64}"
    }


@app.post('/api/v1/auth/verify-2fa')
async def verify_2fa(
    data: TOTP,
    db: Session = Depends(settings.get_db),
    user: User = Depends(get_current_user)
):
    user_secret = user.totp_secret
    if user_secret:
        verified = verify_secret(user_secret, data.totp)
        if verified:
            user = db.query(User).filter(User.email == user.email).first()
            user.two_factor_auth = True
            db.commit()
            return {
                "message": "2FA is enabled now, please login."
            }
        else:
            return {
                "message": "Invalid totp, please try again!"
            }
    else:
        raise HTTPException(status_code=400, detail="Generate totp secret first")