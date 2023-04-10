
from dotenv import load_dotenv
from fastapi import FastAPI

from backend.models.user import Base as TABLE_BASE
from backend.database import DataBase
from sqlalchemy.ext.declarative import declarative_base
from backend.endpoints import (
    create_user_endpoint,
    verify_token_by_mail_endpoint,
    login_user_endpoint,
    user_taxes_data_update_endpoint
)


Base = declarative_base()
load_dotenv()

def create_app():
    app = FastAPI()
    ##Users

    # Crear estructura básica de modelos en base datos
    db = DataBase()

    TABLE_BASE.metadata.create_all(db.engine)

    app.include_router(create_user_endpoint.router)
    app.include_router(verify_token_by_mail_endpoint.router)
    app.include_router(login_user_endpoint.router)
    app.include_router(user_taxes_data_update_endpoint.router)
    return app