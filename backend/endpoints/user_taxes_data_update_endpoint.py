import logging
from pydantic import BaseModel
from pydantic import Field
from fastapi import Depends, status, UploadFile, APIRouter, File
from typing import Dict
from typing import Final
from typing import Any


from backend.usecases import UserTaxesDataCreator
from backend.schemas import UserEmailDefault, UserDataResponse, UserCleanData
from backend.models import User
from backend.database import GetCurrentUsers


router = APIRouter()

UPDATE_USER_TAXES_DATA_ERROR_MESSAGE: Final = "ERROR IN one user ENDPOINT"
USER_TAXES_DATA_ENDPOINT_SUMMARY: Final = "Show one User"
USER_TAXES_DATA_ENDPOINT_PATH: Final = "/user/taxes_data"
DATA_KEY: Final = "data"
SUCCESS_KEY: Final = "success"
TAX_KEY: Final = "taxes_data"

@router.post(
    path=USER_TAXES_DATA_ENDPOINT_PATH,
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary=USER_TAXES_DATA_ENDPOINT_SUMMARY,
    tags=["Users"],
)
async def create_user_taxes_data(
    get_current_user: UserEmailDefault = Depends(GetCurrentUsers.get_current_user),
    file: UploadFile = File(...)
):
    request_data_response = None
    success = False
    try:
        user_tax_data_getter = UserTaxesDataCreator()
        contents = await file.read()
        root = './backend/database/files_root/'
        with open(root+file.filename, "wb") as f:
            f.write(contents)
        response_data = await user_tax_data_getter.run(
            get_current_user,
            root,
            file.filename
        )
        if response_data[0].get('success'):
            user_data = response_data[0].get('user')
            user_data_response = UserCleanData.construct(
                user_id = user_data.user_id,
                name = user_data.name,
                last_name = user_data.last_name,
                mail = user_data.mail,
            ).dict(by_alias=True)
        if response_data[1].get('success'):
            taxes_data = response_data[1].get('taxes_response')
            taxes_data_response = UserDataResponse.construct(
                data_id = taxes_data.data_id,
                identifier = user_data.name,
                tax_filing = taxes_data.tax_filing,
                wages = taxes_data.wages,
                total_deduction = taxes_data.total_deduction,
            ).dict(by_alias=True)
            success = True
            request_data_response = response_data[1].get('data')

        
    except Exception as error:
        logging.error(UPDATE_USER_TAXES_DATA_ERROR_MESSAGE, error)
    return {
        SUCCESS_KEY: success,
        DATA_KEY: request_data_response,
        TAX_KEY: taxes_data_response
    }
