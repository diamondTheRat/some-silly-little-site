from pydantic import BaseModel
from dotenv import load_dotenv
import os
import bcrypt


load_dotenv()

password_hash = os.environ["SITE-PASSWORD"].encode("utf-8")
print(password_hash)
class Command(BaseModel):
    command: str
    

class consoleOutput(BaseModel):
    output: list
    cwd: str
    

class LoginInfo(BaseModel):
    password: str = ""