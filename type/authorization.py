import typing
import strawberry
from conn.db import conn
from models.index import users

from utils.get_user_by_email import get_user_by_email

from type.types import ResponseSuccess
from type.exceptions import CustomException

from utils.hash_password import hash_password


@strawberry.type
class MyProfile:
    id: str
    first_name: str
    last_name: str
    email: str
    password: str
    created_at: str


def get_me() -> MyProfile:
    return conn.execute(users.select().where(users.c.id == id)).fetchone()


@strawberry.type
class TokenResp:
    token: str


def login(email: str, password: str) -> ResponseSuccess[TokenResp]:
    user = get_user_by_email(email)
    print("User ", user)
    if not user:
        raise CustomException(message="Not registered user.", status=401)
    if hash_password(password) == user.password:
        return ResponseSuccess[TokenResp](status=200, message="Authorization", data=TokenResp(token="triqhjakdsjkagjsdgjkahkjdsh"))

    return ResponseSuccess[None](status=401, message="Unauthorized", data=None)
