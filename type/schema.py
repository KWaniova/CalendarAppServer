import typing
import strawberry
from conn.db import conn, engine
from models.index import users, session
from strawberry.types import Info
from type.user import User, get_users, get_user, create_user as create_u, update_user, delete_user
from type.types import ResponseSuccess
from type.authorization import MyProfile, get_me, login, TokenResp


@strawberry.type
class Query:
    user: User = strawberry.field(resolver=get_user)
    users: typing.List[User] = strawberry.field(resolver=get_users)
    me: MyProfile = strawberry.field(resolver=get_me)


@ strawberry.type
class Mutation:

    @strawberry.mutation
    def login(self, email: str, password: str) -> ResponseSuccess[TokenResp]:
        return login(email, password)

    @ strawberry.mutation
    async def create_user(self, first_name: str, last_name: str, email: str, password: str, info: Info) -> ResponseSuccess[None]:
        return await create_u(first_name, last_name, email, password)

    @ strawberry.mutation
    def update_user(self, id: str, first_name: str, last_name: str, email: str) -> ResponseSuccess[None]:
        return update_user(id, first_name, last_name, email)

    @ strawberry.mutation
    def delete_user(self, id: int) -> bool:
        return delete_user(id)
