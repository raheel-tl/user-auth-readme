from jose import jwt
from werkzeug.wrappers import Request, Response

from fastapi import HTTPException, FastAPI


class AuthMiddleware:
    '''
    Simple WSGI middleware for authentication using JWT access token
    '''

    def __init__(self, app: FastAPI, secret_key: str):
        super().__init__(app)
        self.secret_key = secret_key

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
                email = payload.get('sub')
                request.state.user = {'email': email}
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail='Token has expired')
            except jwt.JWTError:
                raise HTTPException(status_code=401, detail='Invalid token')
        else:
            raise HTTPException(status_code=401, detail='Authorization header missing or malformed')

        response = await call_next(request)
        return response
