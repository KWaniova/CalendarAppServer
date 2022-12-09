import typing
import strawberry
from conn.db import conn, engine
from models.index import users, session
from strawberry.types import Info
from type.user import User, get_users, get_user, create_user as create_u, update_user, delete_user
from type.types import ResponseSuccess


@strawberry.type
class Query:
    user: typing.List[User] = strawberry.field(resolver=get_user)
    users: typing.List[User] = strawberry.field(resolver=get_users)


@ strawberry.type
class Mutation:

    @ strawberry.mutation
    async def create_user(self, first_name: str, last_name: str, email: str, password: str, info: Info) -> ResponseSuccess:
        return await create_u(first_name, last_name, email, password)

    @ strawberry.mutation
    def update_user(self, id: str, first_name: str, last_name: str, email: str) -> ResponseSuccess:
        return update_user(id, first_name, last_name, email)

    @ strawberry.mutation
    def delete_user(self, id: int) -> bool:
        return delete_user(id)
