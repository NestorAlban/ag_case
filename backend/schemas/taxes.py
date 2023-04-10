from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from fastapi import Query
from typing import Optional
from datetime import datetime


class UserDataResponse(BaseModel):
    data_id: int = Field(default = 1)
    identifier: str = Field(default = "Sebastian")
    tax_filing:str = Field(default = "Single")
    wages: int = Field(default = 1)
    total_deduction: int = Field(default = 1)