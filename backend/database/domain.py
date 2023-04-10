from dataclasses import dataclass


@dataclass(frozen=True)
class UserDomain:
    user_id: int
    name: str
    last_name: str
    mail: str
    password: str
    active_status: bool

@dataclass(frozen=True)
class UserDataDomain:
    data_id: int
    identifier: int
    tax_filing: str
    wages: int
    total_deduction: int


class Domain:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_user_domain(user):
        user_domain = UserDomain(
            user.user_id,
            user.name,
            user.last_name,
            user.mail,
            user.password,
            user.active_status,
        )
        return user_domain

    @staticmethod
    def create_user_data_domain(user_data):
        user_data_domain = UserDataDomain(
            user_data.data_id,
            user_data.identifier,
            user_data.tax_filing,
            user_data.wages,
            user_data.total_deduction,
        )
        return user_data_domain














