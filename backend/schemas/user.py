from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from fastapi import Query
from typing import Optional
from datetime import datetime

class UserId(BaseModel):
    id: int = Field(default = 1)

class UserEmailDefault(BaseModel):
    email: str = Field(default = "example@email.com")

class UserRegistrationData(BaseModel):
    name: str = Field(default = "User_name")
    last_name: str = Field(default = "User_last_name")
    mail: str = Field(default = "example@email.com")
    password: str = Field(default = "fake_password")

class UserCleanData(BaseModel):
    user_id: int = Field(default =1)
    name: str = Field(default = "User_name")
    last_name: str = Field(default = "User_last_name")
    mail: str = Field(default = "example@email.com")

class LoginData(BaseModel):
    email: str = Field(default = "example@email.com")
    password: str = Field(default = "fake_password")


