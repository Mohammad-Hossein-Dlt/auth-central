from pydantic import BaseModel

class UserRegisterInput(BaseModel):
    email: str
    password: str