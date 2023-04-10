import logging
from fastapi import status
from fastapi import APIRouter, Response, Request
from typing import Final

from backend.usecases import VerifingEmailByToken

router = APIRouter()

VERIFICATION_BY_EMAIL_ERROR_MESSAGE: Final = "ERROR IN verification_by_email ENDPOINT"
VERIFICATION_BY_EMAIL_ENDPOINT_SUMMARY: Final = "verify request_response"
VERIFICATION_BY_EMAIL_ENDPOINT_PATH: Final = "/verification/"
SUCCESS_KEY: Final = "success"
DATA_KEY: Final = "data"
HTTP_404_KEY: Final = 404
HTTP_200_KEY: Final = 200
HTTP_400_KEY: Final = 400

@router.get(
    path=VERIFICATION_BY_EMAIL_ENDPOINT_PATH,
    status_code=status.HTTP_200_OK,
    summary=VERIFICATION_BY_EMAIL_ENDPOINT_SUMMARY,
    tags=["Users"],
)
def verification_by_email_endpoint(request: Request, token: str):
    success = False
    request_response = None
    try:
        email_verify = VerifingEmailByToken()
        request_response = email_verify.run(
            token = token
        )
        print(request_response)
        if request_response:
            success = request_response
    except Exception as error:
        logging.error(VERIFICATION_BY_EMAIL_ERROR_MESSAGE, error)
    return {SUCCESS_KEY: success}

