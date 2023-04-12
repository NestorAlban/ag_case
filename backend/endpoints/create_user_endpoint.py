import logging
from fastapi import status
from fastapi import APIRouter, Response
from typing import Final

from backend.usecases import UserCreatorBySignInUseCase
from backend.schemas import UserRegistrationData
from backend.database import EmailSend

router = APIRouter()

CREATE_USER_ERROR_MESSAGE: Final = "ERROR IN create_user ENDPOINT"
CREATE_USER_ENDPOINT_SUMMARY: Final = "Create a new User"
CREATE_USER_ENDPOINT_PATH: Final = "/create_user"
SUCCESS_KEY: Final = "success"
DATA_KEY: Final = "data"
HTTP_404_KEY: Final = 404
HTTP_201_KEY: Final = 201
HTTP_400_KEY: Final = 400

@router.post(
    path=CREATE_USER_ENDPOINT_PATH,
    status_code=status.HTTP_201_CREATED,
    summary=CREATE_USER_ENDPOINT_SUMMARY,
    tags=["Users"],
)
async def create_user_by_sign_in_endpoint(
    response: Response, 
    new_user_data: UserRegistrationData
):
    success = False
    user_response = None
    try:
        user_creator = UserCreatorBySignInUseCase()
        name = new_user_data.name.strip()
        last_name = new_user_data.last_name.strip()
        mail = new_user_data.mail.strip()
        password = new_user_data.password.strip()
        
        if len(name) != 0 and len(mail) != 0 and len(password) != 0 and len(last_name) != 0:
            user = await user_creator.run(UserRegistrationData(
                name = name, 
                last_name = last_name,
                mail = mail,
                password = password
                )
            )
            if user:
                success = user['success']
                user_response = user['data']
                user_data = user['user']
    except Exception as error:
        response.status_code = HTTP_400_KEY
        logging.error(CREATE_USER_ERROR_MESSAGE, error)
    return {SUCCESS_KEY: success, DATA_KEY: user_response}

