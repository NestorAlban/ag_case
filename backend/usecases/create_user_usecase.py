
from pydantic import Field, BaseModel
from backend.database import UserDomain
from backend.services import UserService
from backend.schemas import UserRegistrationData



class UserCreatorBySignInUseCase:
    def __init__(self):
        pass

    def run(self, params: UserRegistrationData) -> dict:
        user_service = UserService()
        print('==============================bbbbbbbbbb==============================')
        user_response = user_service.create_user_by_sing_in(
            params.name,
            params.last_name,
            params.mail,
            params.password,
        )
        return user_response