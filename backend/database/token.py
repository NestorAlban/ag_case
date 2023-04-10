import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from backend.schemas import TokenData
from backend.models import User

SECRET_KEY = str(os.getenv("SECRET_MAIL"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token():
    def create_access_token(data: dict):
        to_encode = data.copy()
        # expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        # to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(token: str):
        try:
            payload = jwt.decode(str(token), SECRET_KEY, algorithms=ALGORITHM)
            print(payload)
            name = payload.get("username")
            mail = payload.get("email")
            print(name)
            if name is None:
                raise print('credentials exception')
            token_data = TokenData(name=name)
        except JWTError:
            raise print('credentials exception')
        return {'name': name, 'mail': mail}

