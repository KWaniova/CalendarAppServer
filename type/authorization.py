import typing
import strawberry
from conn.db import conn
from models.index import users

from type.types import ResponseSuccess


@strawberry.type
class Me:
    id: str
    first_name: str
    last_name: str
    email: str
    password: str
    created_at: str


@strawberry.type
class Query:
    @strawberry.field
    def me(self) -> Me:
        return conn.execute(users.select().where(users.c.id == id)).fetchone()


@ strawberry.type
class Mutation:
    @ strawberry.mutation
    def login(self, email: str, password: str) -> ResponseSuccess:
        return ResponseSuccess(status=200, message="Authorization", data={
            "token": '9387kjskdhfjshfjhskfhToken'
        })
