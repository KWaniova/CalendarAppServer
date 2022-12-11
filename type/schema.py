import typing
import strawberry
from strawberry.types import Info
from type.user import *
from type.types import ResponseSuccess
from type.authorization import *
from type.is_authenticated_class import IsAuthenticated


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
    def connections(self, auth: str, id: str) -> typing.Optional[typing.List[typing.Union[ConnectionBase, ConnectedUser]]]:
        authorized_user_id = authorized_user(auth)
        if authorized_user_id == id:
            return get_my_connections(id)
        return None


@ strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, email: str, password: str) -> ResponseSuccess[TokenResp]:
        return login(email, password)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def logout(self, auth: str) -> ResponseSuccess[None]:
        return logout(token=auth)

    @ strawberry.mutation
    async def create_user(self, first_name: str, last_name: str, email: str, password: str, info: Info) -> ResponseSuccess[None]:
        return await create_user(first_name, last_name, email, password)

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


# TODO: connections -> user detail for friend is different than for not friend
# events
