from pydantic import BaseModel


class UserDataModel(BaseModel):
    password: str


class UserRegistrationModel(BaseModel):
    username: str
    password: str
