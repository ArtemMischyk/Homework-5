import json
from typing import Any, Optional
from werkzeug.exceptions import HTTPException
from pydantic import BaseModel
from schemas.user import UserDataModel
from core import passwords


class UserStorageModel(BaseModel):
    user_data: dict[str, UserDataModel]


class AuthError(HTTPException):
    code = 401
    description = "Authorization error"


class RegistrationError(HTTPException):
    code = 409
    description = "Registration error"


class UserManager:
        data: UserDataModel

        def __init__(self, filename: str) -> None:
            self.filename = filename
            self.data: Any
            self.read_data()

        def read_data(self) -> None:
            with open(self.filename, "r") as file:
                self.data = json.load(file)

        def write_data(self) -> None:
            with open(self.filename, "w") as file:
                json.dump(self.data.dict(), file)

        def get_user_data(self, username: str) -> Optional[UserDataModel]:
            return self.data.user_data(username)

        def create_user(self, username: str, password: str) -> None:
            user = self.get_user_data(username)

            if user is not None:
                raise RegistrationError(f"User with name {username} already exists")

            self.data[username] = UserDataModel(
                password=password.hash_passwords(password))
            self.write_data()

        def authenticate(self, username: str, password: str) -> UserDataModel:
            """
        Authenticate a user based on his username or password.
        In case of an error, raises AuthError.
        """

            user_data = self.get_user_data(username)
            if user_data is None:
                raise AuthError(f"User with name {username} does not exist")

            if not passwords.passwords_equal(password, user_data.password):
                raise AuthError(f"Password for user {username} is not correct")

            return user_data