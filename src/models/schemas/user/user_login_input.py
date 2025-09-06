from pydantic import BaseModel

class UserLoginInput(BaseModel):
    username: str
    password: str