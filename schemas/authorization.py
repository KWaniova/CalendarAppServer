import strawberry
from conn.db import conn
from models.index import users, Token, session


from utils.get_user_by_email import get_user_by_email

from type.types import ResponseSuccess
from schemas.exceptions import CustomException

from utils.hash_password import hash_password
from sqlalchemy import *
from schemas.connection import *


@strawberry.type
class MyProfile:
    id: str
    first_name: str
    last_name: str
    email: str
    password: str
    created_at: str


def get_me(token: str) -> MyProfile:
    user_id = authorized_user(token)
    return conn.execute(users.select().where(users.c.id == user_id)).fetchone()


@strawberry.type
class TokenResp:
    token: str
    id: str


def authorized_user(token):
    user_id = session.execute(select(Token.user_id).where(
        token == Token.token)).scalar()
    if not token:
        raise CustomException(message="Unauthorized user!", status=401)
    return user_id


def login(email: str, password: str) -> ResponseSuccess[TokenResp]:
    user = get_user_by_email(email)
    if not user:
        raise CustomException(message="Not registered user.", status=401)
    if hash_password(password) == user.password:
        token_obj = session.execute(select(Token).where(
            user.id == Token.user_id)).scalar()
        if not token_obj:
            token_obj = Token(password=user.password, id=user.id)
            session.add(token_obj)
            session.commit()
        user_id = authorized_user(token_obj.token)
        return ResponseSuccess[TokenResp](status=200, message="Authorization", data=TokenResp(token=token_obj.token, id=user_id))

    return ResponseSuccess[None](status=401, message="Unauthorized", data=None)


def logout(token: str) -> ResponseSuccess[None]:
    session.execute(delete(Token).where(
        Token.token == token).execution_options(synchronize_session="fetch"))
    session.commit()
    return ResponseSuccess[None](status=200, message="Logged out", data=None)
