import typing
import strawberry
from strawberry.types import Info
from schemas.user import *
from type.types import ResponseSuccess
from schemas.authorization import *
from schemas.authentication_class import IsAuthenticated
from type.user import UserInput


class CreateEventInput:
    title: str
    description: str
    type: str  # TODO enum
    created_at: str


@strawberry.type
class Query:
    user: User = strawberry.field(
        permission_classes=[IsAuthenticated], resolver=get_user)
    users: typing.List[User] = strawberry.field(
        permission_classes=[IsAuthenticated], resolver=get_users)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, auth: str) -> MyProfile:
        return get_me(token=auth)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def my_connections(self, auth: str) -> typing.Optional[ConnectionResponseObj]:
        authorized_user_id = authorized_user(auth)
        return get_my_connections(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connections_list(self, auth: str, user_id: str) -> typing.Optional[ConnectionResponseObj]:
        authorized_user_id = authorized_user(auth)
        if authorized_user_id == user_id:
            return get_my_connections(user_id)
        return get_user_connections(user_id)


@ strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, email: str, password: str) -> ResponseSuccess[TokenResp]:
        return login(email, password)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def logout(self, auth: str) -> ResponseSuccess[None]:
        return logout(token=auth)

    @ strawberry.mutation
    async def create_user(self, user: UserInput, info: Info) -> ResponseSuccess[None]:
        return await create_user(user)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def edit(self, auth: str, first_name: str, last_name: str, email: str) -> ResponseSuccess[None]:
        id = authorized_user(auth)  # can be stored in session context???
        return update_user(id, first_name, last_name, email)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_me(self, auth: str, id: int) -> bool:
        id = authorized_user(auth)  # can be stored in session context???
        return delete_user(id)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_connection(self, auth: str, target_user_id: str) -> bool:
        id = authorized_user(auth)  # can be stored in session context???
        return add_connection(source_user_id=id, target_user_id=target_user_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def connection_action(self, auth: str, connection_id: str, action: ConnectionAction) -> bool:
        return connection_action(connection_id, action)

    def create_event(self, auth: str, event: CreateEventInput) -> bool:
        return True


# TODO: connections -> user detail for friend is different than for not friend
# events

# TODO: add proper request response
