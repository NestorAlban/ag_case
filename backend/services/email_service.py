from backend.database import DataBase


class EmailService:
    def __init__(self):
        self.database = DataBase()
        pass

    def verify_token_by_email(
        self,
        token: str
    ):
        request_response = None
        print('==============================ccccccccccc==============================')
        request_response = self.database.verify_token_by_email(
            token = token,
        )
        return request_response