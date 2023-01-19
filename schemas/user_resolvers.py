import typing
import strawberry
from conn.db import conn
from models.index import users, session
from models.user import User as UserType
from type.types import ResponseSuccess
from type.user import UserInput
from sqlalchemy.orm import *
from enum import Enum
from type.types import Resolver


@strawberry.enum
class UserConnectionType(Enum):
    CONNECTED = "connected"


@strawberry.type
class User:
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: str


class UserResolver(Resolver):
    def get_user(self, auth: str, id: str) -> User:
        return conn.execute(users.select().where(users.c.id == id)).fetchone()

    def get_users(self, auth: str) -> typing.List[User]:
        return conn.execute(users.select()).fetchall()

    async def create_user(self, user: UserInput) -> ResponseSuccess[None]:
        userObj = UserType(first_name=user.first_name, last_name=user.last_name,
                           email=user.email, password=user.password)
        with session:
            session.add(userObj)
            session.commit()
        return ResponseSuccess[None](status=201, message="created", data=None)

    def update_user(self, id: str, first_name: str, last_name: str, email: str) -> ResponseSuccess[None]:
        conn.execute(users.update().where(users.c.id == id), {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        })
        return ResponseSuccess[None](status=200, message="updated", data=None)

    def delete_user(self, id: str) -> ResponseSuccess[None]:
        conn.execute(users.delete().where(users.c.id == id))
        return ResponseSuccess[None](status=200, message="deleted", data=None)
