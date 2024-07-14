from pydantic import BaseModel


class Command(BaseModel):
    command: str
    

class consoleOutput(BaseModel):
    output: list
    cwd: str