from backend.services import UserService, TaxesService
from backend.models import User
from pydantic import Field
from backend.schemas import UserEmailDefault

class UserTaxesDataCreator:
    def __init__(self):
        pass

    async def run(self, email, file, filename) -> User:
        user_service = UserService()
        taxes_service = TaxesService()
        taxes = None
        taxes_response =None
        user = user_service.get_user_by_email(email)
        if user.get('success'):
            user_id = user.get('user').user_id
            taxes = await taxes_service.get_taxes_data_by_file(
                file,
                user_id,
                filename
            )
            if taxes.get('success'):
                taxes_response = taxes

        return [user, taxes_response]