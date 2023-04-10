from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm
)
from .token import Token
from .database import DataBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

class GetCurrentUsers():
    def get_current_user(token: str = Depends(oauth2_scheme)):
        print(token)
        print('token==============================')
        # credentials_exception = HTTPException(
        #     status_code = status.HTTP_401_UNAUTHORIZED,
        #     detail = "Could not validate credentials",
        #     headers = {"WWW-Authenticate": "Bearer"}
        # )
        token_res = Token.verify_token(
            token
        )
        print(token_res.get('name'))
        return token_res.get('mail')

