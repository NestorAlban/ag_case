import logging
import os
from typing import Final
import fitz
import io

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import *
from .domain import *
from .token import Token
from .hash_pass import Hash_Password
from .email import EmailSend
from .import_tax_data import FileData

logger = logging.getLogger(__name__)
logger.level = logger.setLevel(logging.INFO)
DATABASE_CONNECTION_ERROR: Final = "Error while connecting to PostgreSQL"
CLOSED_DATABASE_MESSAGE: Final = "PostgreSQL connection is closed"
CONNECTING_DB_MESSAGE: Final = "Connecting PostgreSQL database======"
DELETED_USER: Final = False
ACTIVE_USER: Final = True
ACTIVE_PRODUCT: Final = True
DEACTIVATE_PRODUCT: Final = False
CANNOT_PROCEED_MESSAGE: Final = "Cannot proceed: "
SPACES_FOR_MESSAGE: Final = "============================"

class DataBaseException(Exception):
    code: int = 400
    errors: str = "could not connect to db"


class DataBase:
    def __init__(self) -> None:
        try:
            self.database_user = os.getenv("DATABASE_USER")
            self.database_password = os.getenv("DATABASE_PASSWORD")
            self.database_host = os.getenv("DATABASE_HOST")
            self.database_port = os.getenv("DATABASE_PORT")
            self.database_name = os.getenv("DATABASE_NAME")
            self.engine = create_engine(
                f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}",
                echo=True,
                future=True,
            )
            Session = sessionmaker(self.engine)
            self.session = Session()
        except Exception as database_exception:
            logging.exception(database_exception)
            raise DataBaseException()


    def login_user(
        self, 
        email: str, 
        password: str
    ):
        user = None
        token_value = None
        token_type = None
        try:
            user = self.session.query(
                User
            ).filter(
                User.mail == email
            ).first()
            if user and user.active_status == True:
                user_domain= Domain.create_user_domain(user)
                print(user_domain.password)
                print(password)
                
                if Hash_Password.verify_pass(
                    user_domain.password,
                    password
                ):
                    access_token = Token.create_access_token(
                        data={
                            'username': user_domain.name,
                            "email": user_domain.mail,
                        }
                    )
                    token_value = access_token
                    token_type = "bearer"
            
            
            self.session.close()
        except Exception as database_exception:
            logging.exception(database_exception)

            raise DataBaseException()
        
        return {"user": user, "token": (token_value, token_type)}
    
    async def create_user_sign_in(
        self, 
        name: str, 
        last_name: str,
        mail: str,
        password: str,
    ):
        user = None
        success = False
        data = 'None'
        
        try:
            
            print(name, last_name, mail, password)
            user_verification = self.session.query(
                User
            ).filter(
                User.name == name
            ).first()
            if user_verification and not user_verification.active_status:
                data = 'The user is already created, but has not been verified.'
            elif user_verification and user_verification.active_status:
                data = 'The user is already created and has been verified.'
            else:
                user = User(
                    name = name, 
                    last_name = last_name,
                    mail = mail,
                    password = Hash_Password.bcrypt_pass(password)
                )
                send_ver = await EmailSend.send_email_smt(email=[mail], instance=user)
                if send_ver:
                    self.session.add(user)
                    self.session.commit()
                    success = True
                    data = 'The user was created, please check you mail inbox to verify it.'
        except Exception as database_exception:
            logging.exception(database_exception)

            raise DataBaseException()
        self.session.close()
        return {'success': success, 'data': data, 'user': user}
    
    def get_user_by_email(
        self, 
        mail: str,
    ):
        user = None
        success = False
        try:
            print('get user by email')
            user = self.session.query(
                User
            ).filter(
                User.mail == mail
            ).first()
            print(user)
            success = True
            self.session.close()
        except Exception as database_exception:
            logging.exception(database_exception)

            raise DataBaseException()
        
        return {'success':success, "user": user}

    def verify_token_by_email(
        self, 
        token: str,
    ):
        user = None
        token_value = None
        token_type = None
        success = False
        token_data = Token.verify_token(token)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(token_data)
        try:

            user = self.session.query(
                User
            ).filter(
                User.mail == token_data.get("mail")
            ).first()
            if user and not user.active_status:
                user.active_status = True
                self.session.commit()
                success = True
        except Exception as database_exception:
            logging.exception(database_exception)

            raise DataBaseException()
        return {'success': success}


    async def get_taxes_data_by_file(
        self, 
        file,
        user_id:int, 
        filename
    ):
        taxes_response = None
        taxes = None
        taxes_data_verify = None
        success = False
        data = None
        try:
            taxes_va = FileData.start_file_reader(file_path= file, filename=filename)
            print(taxes_va)
            taxes_data_verify = self.session.query(
                UserData
            ).filter(
                UserData.identifier == User.user_id
            ).first()
            if taxes_data_verify:
                data = "The data was created before this request."
                taxes_response = taxes_data_verify
            elif not taxes_data_verify:
                taxes = UserData(
                    identifier = user_id,
                    tax_filing = taxes_va.get('text1'),
                    wages = taxes_va.get('text3'),
                    total_deduction = taxes_va.get('text2')
                )
                if taxes:
                    self.session.add(taxes)
                    self.session.commit()
                    success = True
                    taxes_response = taxes
                    data = 'The data was created, please verify it.'

            success = True
            self.session.close()
        except Exception as database_exception:
            logging.exception(database_exception)

            raise DataBaseException()
        
        return {'success':success, 'data':data, "taxes_response": taxes_response}


