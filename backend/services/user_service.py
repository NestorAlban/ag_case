from backend.database import DataBase


class UserService:
    def __init__(self):
        self.database = DataBase()
        pass
    
    def login_user(
        self, 
        email: str, 
        password: str
    ):
        user = self.database.login_user(
            email, 
            password
        )
        return user

    def create_user_by_sing_in(
        self,
        name: str, 
        last_name: str,
        mail: str,
        password: str,
    ):
        user_response = None
        user_response = self.database.create_user_sign_in(
            name = name, 
            last_name = last_name,
            mail = mail,
            password = password,
        )
        return user_response
    
    def get_user_by_email(
        self,
        mail: str,
    ):
        user_response = None
        user_response = self.database.get_user_by_email(
            mail = mail,
        )
        return user_response
