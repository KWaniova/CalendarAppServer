import typing
import strawberry
from conn.db import conn, engine
from models.index import users, session
from strawberry.types import Info
from models.user import User as UserType
from strawberry.http import GraphQLHTTPResponse

from fastapi import FastAPI, HTTPException


@strawberry.type
class ResponseSuccess:
    status: int
    data: typing.Optional[str]


@strawberry.type
class User:
    id: str
    first_name: str
    last_name: str
    email: str
    password: str


@strawberry.type
class Query:
    @strawberry.field
    def user(id: str) -> User:
        return conn.execute(users.select().where(users.c.id == 1)).fetchone()

    @strawberry.field
    def users(self) -> typing.List[User]:
        # existss = session.query(User.id).filter_by(id=1).first()
        # exists = conn.execute(users.select(users.c.id).where(users.c.id == 1)).first()
        # print(f"existss: ",existss)
        # print(f"exists: ",exists)
        return conn.execute(users.select()).fetchall()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_flavour(self, name: str, info: Info) -> bool:
        return True

    @strawberry.mutation
    async def create_user(self, first_name: str, last_name: str, email: str, password: str, info: Info) -> ResponseSuccess:
        try:
            with session:
                userObj = UserType(first_name, last_name,
                                   email=email, password=password)
                session.add(userObj)
                session.commit()
        except:
            raise HTTPException(status_code=500, detail="Problem")

        return ResponseSuccess(status=200, data=None)

    @strawberry.mutation
    def update_user(self, id: int, first_name: str, last_name: str, email: str, password: str, info: Info) -> str:
        userObj = UserType(first_name, last_name,
                           email=email, password=password)

        result = conn.execute(users.update().where(users.c.id == id), {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        })
        print(result. returns_rows)
        return str(result.rowcount) + " Row(s) updated"
        # try:
        #     with session:
        #         userObj = UserType(first_name, last_name,
        #                            email=email, password=password)
        #         items = session.query(UserType).filter(UserType.id == id)
        #         print(items)
        #         session.update({UserType.name: "NAME"})
        #         session.commit()
        # except:
        #     raise HTTPException(status_code=500, detail="Problem")

        # return ResponseSuccess(status=200, data=None)

    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        result = conn.execute(users.delete().where(users.c.id == id))
        return result.rowcount > 0
