from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

class Hash_Password():
    
    def bcrypt_pass(password: str):

        return pwd_cxt.hash(password)

    def verify_pass(hass_pass, hassnt_pass):
        return pwd_cxt.verify(
            hassnt_pass,
            hass_pass
        )
    
test_pas = 'fake_password'

print(pwd_cxt.hash(test_pas))