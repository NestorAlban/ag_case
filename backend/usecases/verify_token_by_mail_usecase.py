
from pydantic import Field, BaseModel
from backend.services import EmailService



class VerifingEmailByToken:
    def __init__(self):
        pass

    def run(self, token: str) -> dict:
        email_service = EmailService()
        print('==============================bbbbbbbbbb==============================')
        request_response = email_service.verify_token_by_email(
            token = token,
        )
        return request_response