import typing
import strawberry
from strawberry.types import Info
from schemas.user_resolvers import *
from type.types import ResponseSuccess
from schemas.user_resolvers import UserResolver
from schemas.connection_resolvers import ConnectionResolver, ConnectionResponse, ConnectionAction, NotConnectedUser
from schemas.authorization_resolvers import AuthorizationResolver, MyProfile, TokenResp
from schemas.events_resolvers import EventResolver
from schemas.authentication_class import IsAuthenticated
from classes.event import Event, EventTypeEnum, EventInput, EventInputUpdate
from type.user import UserInput


@strawberry.type
class Query:
    user: User = strawberry.field(
        permission_classes=[IsAuthenticated], resolver=UserResolver().get_user)
    users: typing.List[User] = strawberry.field(
        permission_classes=[IsAuthenticated], resolver=UserResolver().get_users)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connections(self, auth: str) -> ConnectionResponse:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        connection_resolver = ConnectionResolver()
        return connection_resolver.get_user_connections(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, auth: str) -> MyProfile:
        auth_resolver = AuthorizationResolver()
        return auth_resolver.get_me(token=auth)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_not_connected_users(self, auth: str) -> typing.List[NotConnectedUser]:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        connection_resolver = ConnectionResolver()
        return connection_resolver.get_not_connected_users_to_user(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connection_requests(self, auth: str) -> ConnectionResponse:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        connection_resolver = ConnectionResolver()
        return connection_resolver.get_user_connection_requests(authorized_user_id)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def connection_requests_sent(self, auth: str) -> ConnectionResponse:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        connection_resolver = ConnectionResolver()
        sent = connection_resolver.get_user_connection_requests_sent(
            authorized_user_id)
        return sent

    @strawberry.field(permission_classes=[IsAuthenticated])
    def my_events(self, auth: str, from_date: str, to_date: str) -> typing.List[Event]:
        events_resolver = EventResolver()
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        return events_resolver.get_events_in_date_range(id=authorized_user_id, from_date=from_date, to_date=to_date)


@ strawberry.type
class Mutation:
    @strawberry.mutation
    def login(self, email: str, password: str) -> ResponseSuccess[TokenResp]:
        auth_resolver = AuthorizationResolver()
        return auth_resolver.login(email, password)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def logout(self, auth: str) -> ResponseSuccess[None]:
        auth_resolver = AuthorizationResolver()

        return auth_resolver.logout(token=auth)

    @ strawberry.mutation
    async def create_user(self, user: UserInput, info: Info) -> ResponseSuccess[None]:
        user_resolver = UserResolver()
        return await user_resolver.create_user(user)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def edit(self, auth: str, first_name: str, last_name: str, email: str) -> ResponseSuccess[None]:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        user_resolver = UserResolver()
        return user_resolver.update_user(authorized_user_id, first_name, last_name, email)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_me(self, auth: str, id: int) -> bool:
        auth_resolver = AuthorizationResolver()
        user_resolver = UserResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        return user_resolver.delete_user(authorized_user_id)

    @ strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_connection(self, auth: str, target_user_id: str) -> bool:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        connection_resolver = ConnectionResolver()

        return connection_resolver.add_connection(source_user_id=authorized_user_id, target_user_id=target_user_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def connection_action(self, auth: str, connection_id: str, action: ConnectionAction) -> bool:
        connection_resolver = ConnectionResolver()
        return connection_resolver.connection_action(connection_id, action)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_private_event(self, auth: str, event: EventInput) -> ResponseSuccess[str]:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        events_resolver = EventResolver()
        return events_resolver.create_event(authorized_user_id, type=EventTypeEnum.PRIVATE, event=event)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_public_event(self, auth: str, event: EventInput) -> ResponseSuccess[str]:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        events_resolver = EventResolver()
        return events_resolver.create_event(authorized_user_id, type=EventTypeEnum.PUBLIC, event=event)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_event(self, auth: str, event: EventInputUpdate) -> ResponseSuccess[None]:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        events_resolver = EventResolver()
        return events_resolver.update_event(authorized_user_id, event_to_update=event)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_event(self, auth: str, id: str) -> bool:
        auth_resolver = AuthorizationResolver()
        authorized_user_id = auth_resolver.get_authorized_user_id(auth)
        if authorized_user_id:
            events_resolver = EventResolver()
            return events_resolver.delete_event(authorized_user_id, id)
