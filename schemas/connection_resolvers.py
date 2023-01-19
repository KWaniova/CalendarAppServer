import typing
import strawberry
from models.index import session
from models.user import User as UserType
from schemas.exceptions import CustomException

from models.connection import Connection as ConnectionModel, ConnectionStatus

from sqlalchemy import *
from sqlalchemy.orm import *
from enum import Enum
from type.types import BaseMapper
from type.types import Resolver


@strawberry.enum
class ConnectionAction(Enum):
    ACCEPT = "accept"
    DECLINE = "decline"
    DISCONNECT = "disconnect"


@strawberry.type
class ConnectionBase:
    id: str
    user_id: str
    first_name: str
    last_name: str
    created_at: str
    connection_status: typing.Optional[ConnectionStatus]


@strawberry.type
class UserBase(UserType):
    id: str
    first_name: str
    last_name: str
    created_at: str


@strawberry.type
class ConnectionResponseObj:
    connections: typing.List[ConnectionBase]
    connection_requests: typing.Optional[typing.List[ConnectionBase]] = None
    connection_requests_sent: typing.Optional[typing.List[ConnectionBase]] = None


@strawberry.type
class ConnectionResponse:
    connections: typing.List[ConnectionBase] = None


@strawberry.type
class NotConnectedUser:
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: str


@strawberry.type
class ConnectedUser:
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: str


class ConnectionsMapper(BaseMapper):
    def map_to_entity(self, row) -> ConnectionBase:
        conn_user: UserBase = row[0]
        return ConnectionBase(user_id=conn_user.id, created_at=conn_user.created_at, first_name=conn_user.first_name,
                              last_name=conn_user.last_name, id=row[1], connection_status=row[2])


class ConnectionCriteriaMapper:
    def get_query_for_user_as_target(self, user_id):
        # PATTERN: Query Object
        return select(UserBase, ConnectionModel.id, ConnectionModel.status).filter(
            ConnectionModel.target_user_id == user_id).where(UserType.id == ConnectionModel.source_user_id)

    def get_query_for_user_as_source(self, user_id):
        return select(UserBase, ConnectionModel.id, ConnectionModel.status).filter(
            ConnectionModel.source_user_id == user_id).where(
            ConnectionModel.target_user_id == UserType.id)


class ConnectionResolver(Resolver):
    def __init__(self):
        self.criteria_mapper = ConnectionCriteriaMapper()

    def get_not_connected_users_to_user(self, id: str):
        not_connected_users = session.query(UserType).filter(UserType.id != id).where(not_(exists().where(ConnectionModel.target_user_id == id).where(
            ConnectionModel.source_user_id == UserType.id))).where(not_(exists().where(ConnectionModel.source_user_id == id).where(ConnectionModel.target_user_id == UserType.id)))
        if not not_connected_users:
            return []

        return not_connected_users

    def get_user_connection_requests(self, id: str):
        query_target_connection_requests = self.criteria_mapper.get_query_for_user_as_target(
            id).where(ConnectionModel.status == ConnectionStatus.to_accept)
        connection_requests = session.execute(
            query_target_connection_requests).fetchall()
        if not connection_requests:
            return ConnectionResponse(connections=[])
        return ConnectionResponse(connections=self._get_conn_list_from_rows(connection_requests))

    def get_user_connection_requests_sent(self, id: str):
        query_source_connection_requests = self.criteria_mapper.get_query_for_user_as_source(
            id).where(ConnectionModel.status == ConnectionStatus.to_accept)
        connection_requests_sent = session.execute(
            query_source_connection_requests).fetchall()
        if not connection_requests_sent:
            return ConnectionResponse(connections=[])
        return ConnectionResponse(connections=self._get_conn_list_from_rows(connection_requests_sent))

    def get_user_connections(self, id: str):
        criteria_mapper = ConnectionCriteriaMapper()
        query_target_connections = criteria_mapper.get_query_for_user_as_target(
            id).where(ConnectionModel.status == ConnectionStatus.connected)
        query_source_connections = criteria_mapper.get_query_for_user_as_source(
            id).where(ConnectionModel.status == ConnectionStatus.connected)
        connections_full_1 = session.execute(
            query_target_connections).fetchall()
        connections_full_2 = session.execute(
            query_source_connections).fetchall()
        result = self._get_conn_list_from_rows(
            [*connections_full_1, *connections_full_2])
        return ConnectionResponse(connections=result)

    def add_connection(self, source_user_id: str, target_user_id: str):
        self._check_if_users_exists(source_user_id, target_user_id)
        self._check_if_conn_exists(source_user_id, target_user_id)
        connectioObj = ConnectionModel(source_user_id, target_user_id)
        session.add(connectioObj)
        session.commit()
        return True

    def connection_action(self, connection_id: str, action: ConnectionAction) -> bool:
        status = session.execute(select(ConnectionModel.status).where(
            ConnectionModel.id == connection_id)).scalar()
        if status == ConnectionStatus.to_accept:
            if action == ConnectionAction.ACCEPT:
                session.execute(update(ConnectionModel).where(ConnectionModel.id ==
                                                              connection_id), {"status": ConnectionStatus.connected})
            elif action == ConnectionAction.DECLINE:
                session.execute(delete(ConnectionModel).where(ConnectionModel.id ==
                                                              connection_id))
            session.commit()
            return True
        if status == ConnectionStatus.connected:
            session.execute(delete(ConnectionModel).where(ConnectionModel.id ==
                                                          connection_id))
            session.commit()
            return True
        return False

    def _get_conn_list_from_rows(self, rows) -> typing.List[ConnectionBase]:
        tab: typing.List[ConnectionBase] = []
        for row in rows:
            conn_mapper = ConnectionsMapper()
            tab.append(conn_mapper.map_to_entity(row))
        return tab

    def _check_if_conn_exists(self, source_user_id: str, target_user_id: str):
        query = select(ConnectionModel.id).where(
            or_(and_(ConnectionModel.source_user_id == source_user_id, ConnectionModel.target_user_id == target_user_id), and_(ConnectionModel.source_user_id == target_user_id, ConnectionModel.target_user_id == source_user_id)))
        connection_exists = session.execute(query).scalar()
        if connection_exists:
            raise CustomException(message="Connection already exists")

    def _check_if_users_exists(self, source_user_id: str, target_user_id: str):
        user_source_present = session.execute(
            select(UserType.id).where(UserType.id == source_user_id)).scalar()
        user_target_present = session.execute(
            select(UserType.id).where(UserType.id == target_user_id)).scalar()
        if not user_source_present and not user_target_present:
            raise CustomException(message="No such user in DB")
