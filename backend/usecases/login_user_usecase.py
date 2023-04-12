from backend.services import UserService
from backend.models import User
from pydantic import Field
from backend.schemas import LoginData, UserCleanData

class LoginUser:
    def __init__(self):
        LoginData
        pass

    def run(self, params: LoginData) -> User:
        user_service = UserService()
        user = user_service.login_user(
            params.email, 
            params.password
        )
        d = user.get('user')
        if d != None:
            login_user_response = UserCleanData(
                **d.__dict__
            )
        return user