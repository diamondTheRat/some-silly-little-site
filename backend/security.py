from data_types import password_hash
import bcrypt


def verify_password(password: str) -> bool:
    if type(password) is not str:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), password_hash) 