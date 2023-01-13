import typing
import strawberry
from conn.db import conn
from models.index import users, session
from models.user import User as UserType
from type.types import ResponseSuccess
from type.user import UserInput
from schemas.authorization import *
from sqlalchemy.orm import *


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


# TODO: by different user type return different obj
def get_user(auth: str, id: str) -> User:
    authorized_user_id = authorized_user(auth)
    connections_query = select(Connection.id, Connection.status).filter(or_(Connection.target_user_id == authorized_user_id, Connection.source_user_id == authorized_user_id)
                                                                        ).where(Connection.status == ConnectionStatus.connected).where(or_(Connection.target_user_id == id, Connection.source_user_id == id))
    connections = session.execute(connections_query).fetchall()
    print("FRIENDS: ", connections)
    return conn.execute(users.select().where(users.c.id == id)).fetchone()


def get_users(auth: str) -> typing.List[User]:
    return conn.execute(users.select()).fetchall()


async def create_user(user: UserInput) -> ResponseSuccess[None]:
    userObj = UserType(first_name=user.first_name, last_name=user.last_name,
                       email=user.email, password=user.password)
    with session:
        session.add(userObj)
        session.commit()
    return ResponseSuccess[None](status=201, message="created", data=None)


def update_user(id: str, first_name: str, last_name: str, email: str) -> ResponseSuccess[None]:
    result = conn.execute(users.update().where(users.c.id == id), {  # TODO: DTO???
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    })
    return ResponseSuccess[None](status=201, message=str(result.rowcount) + " Row(s) updated", data=None)


def delete_user(id: int) -> bool:
    result = conn.execute(users.delete().where(users.c.id == id))

    return result.rowcount > 0
