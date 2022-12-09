import typing
from conn.db import conn
from models.index import users
from models.user import User


def get_user_by_email(email) -> typing.Union[User, None]:
    return conn.execute(users.select().where(users.c.email == email)).fetchone()
