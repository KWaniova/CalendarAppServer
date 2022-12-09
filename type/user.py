import typing
import strawberry
from conn.db import conn, engine
from models.index import users, session
from strawberry.types import Info
from models.user import User as UserType


@strawberry.type
class ResponseSuccess:
    status: int
    data: typing.Optional[str]
    message: str


@strawberry.type
class User:
    id: str
    first_name: str
    last_name: str
    email: str
    password: str
    created_at: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: str, info: Info) -> User:
        print("Context: ", info.context)
        print("Self: ", self)
        return conn.execute(users.select().where(users.c.id == id)).fetchone()

    @ strawberry.field
    def users(self) -> typing.List[User]:
        return conn.execute(users.select()).fetchall()


@ strawberry.type
class Mutation:
    @ strawberry.mutation
    def create_flavour(self, name: str, info: Info) -> bool:
        return True

    @ strawberry.mutation
    async def create_user(self, first_name: str, last_name: str, email: str, password: str, info: Info) -> ResponseSuccess:
        userObj = UserType(first_name=first_name, last_name=last_name,
                           email=email, password=password)
        print(userObj)
        # try:
        with session:
            session.add(userObj)
            session.commit()
        # except:
        #     raise HTTPException(status_code=500, detail="Problem")

        return ResponseSuccess(status=201, message="created", data=None)

    @ strawberry.mutation
    def update_user(self, id: str, first_name: str, last_name: str, email: str) -> ResponseSuccess:

        result = conn.execute(users.update().where(users.c.id == id), {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        })
        return ResponseSuccess(status=201, message=str(result.rowcount) + " Row(s) updated", data=None)

    @ strawberry.mutation
    def delete_user(self, id: int) -> bool:
        result = conn.execute(users.delete().where(users.c.id == id))
        return result.rowcount > 0
