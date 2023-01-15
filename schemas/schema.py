import typing
import strawberry
from strawberry.types import Info
from schemas.user import *
from type.types import ResponseSuccess
from schemas.authorization import *
from schemas.events_resolvers import get_my_events, create_event, update_event, delete_event, Event, EventTypeEnum, EventInput, EventInputUpdate
from schemas.authentication_class import IsAuthenticated
from type.user import UserInput


@strawberry.type
class Query:
    user: User = strawberry.field(
        permission_classes=[IsAuthenticated], resolver=get_user)
    users: typing.List[User] = strawberry.field(
        permission_classes=[IsAuthenticated], resolver=get_users)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connections(self, auth: str) -> ConnectionResponse:
        authorized_user_id = authorized_user(auth)
        return get_user_connections(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, auth: str) -> MyProfile:
        return get_me(token=auth)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_not_connected_users(self, auth: str) -> typing.List[NotConnectedUser]:
        authorized_user_id = authorized_user(auth)
        return get_not_connected_users_to_user(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connection_requests(self, auth: str) -> ConnectionResponse:
        authorized_user_id = authorized_user(auth)
        return get_user_connection_requests(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connection_requests_sent(self, auth: str) -> ConnectionResponse:
        authorized_user_id = authorized_user(auth)
        sent = get_user_connection_requests_sent(authorized_user_id)
        print("SENT: ", sent)
        return sent

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connections_list(self, auth: str, user_id: str) -> typing.Optional[ConnectionResponseObj]:
        authorized_user_id = authorized_user(auth)
        if authorized_user_id == user_id:
            return get_my_connections(user_id)
        return get_user_connections(user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def my_events(self, auth: str, from_date: str, to_date: str) -> typing.List[Event]:
        authorized_user_id = authorized_user(auth)
        return get_my_events(id=authorized_user_id, from_date=from_date, to_date=to_date)


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
        id = authorized_user(auth)
        return update_user(id, first_name, last_name, email)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_me(self, auth: str, id: int) -> bool:
        id = authorized_user(auth)
        return delete_user(id)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_connection(self, auth: str, target_user_id: str) -> bool:
        id = authorized_user(auth)
        return add_connection(source_user_id=id, target_user_id=target_user_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def connection_action(self, auth: str, connection_id: str, action: ConnectionAction) -> bool:
        return connection_action(connection_id, action)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_private_event(self, auth: str, event: EventInput) -> ResponseSuccess[str]:
        id = authorized_user(auth)
        return create_event(id, type=EventTypeEnum.PRIVATE, event=event)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_public_event(self, auth: str, event: EventInput) -> ResponseSuccess[str]:
        id = authorized_user(auth)
        return create_event(id, type=EventTypeEnum.PUBLIC, event=event)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_event(self, auth: str, event: EventInputUpdate) -> ResponseSuccess[None]:
        id = authorized_user(auth)
        return update_event(id, event_to_update=event)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_event(self, auth: str, id: str) -> bool:
        userID = authorized_user(auth)
        if userID:
            return delete_event(userID, id)
