from enum import Enum
from pydantic import BaseModel, EmailStr
from fastapi import Query
from typing import Optional, List
from datetime import datetime



class EmailSchema(BaseModel):
    email: List[EmailStr]

class EmailMessageSchema(BaseModel):
    email: List[EmailStr]




