import typing
import strawberry
from models.index import connections, session, Connection
from models.user import User as UserType
from schemas.exceptions import CustomException

from models.connection import Connection, ConnectionStatus

from sqlalchemy import *
from sqlalchemy.orm import *
from enum import Enum


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
    connection_status: typing.Optional[ConnectionStatus]


@strawberry.type
class UserBase(UserType):
    id: str
    first_name: str
    last_name: str


@strawberry.type
class ConnectionResponseObj:
    connections: typing.List[ConnectionBase]
    connection_requests: typing.Optional[typing.List[ConnectionBase]] = None
    connection_requests_sent: typing.Optional[typing.List[ConnectionBase]] = None


@strawberry.type
class NotConnectedUser:
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: str
    # shared_connections: typing.List[ConnectionBase]


@strawberry.type
class ConnectedUser:
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: str
    # connections: typing.List[ConnectionBase] #TODO: add resolver for field
    # events: typing.List[ConnectionBase] #TODO


def get_conn_list_from_rows(rows) -> ConnectionBase:
    tab: typing.List[ConnectionBase] = []
    for row in rows:
        print("ROW: ", row)
        conn_user: UserBase = row[0]
        tab.append(ConnectionBase(user_id=conn_user.id, first_name=conn_user.first_name,
                   last_name=conn_user.last_name, id=row[1], connection_status=row[2]))
    return tab

# TODO: - special type for connections that are connected or not


def get_my_connections(id) -> typing.Optional[ConnectionResponseObj]:
    query_target_connections = select(UserBase, Connection.id, Connection.status).filter(
        Connection.target_user_id == id).where(UserType.id == Connection.source_user_id).where(Connection.status == ConnectionStatus.connected)
    query_target_connection_requests = select(UserBase, Connection.id, Connection.status).filter(
        Connection.target_user_id == id).where(UserType.id == Connection.source_user_id).where(Connection.status == ConnectionStatus.to_accept)
    query_source_connections = select(UserBase, Connection.id, Connection.status).filter(
        Connection.source_user_id == id).where(
        Connection.target_user_id == UserType.id).where(Connection.status == ConnectionStatus.connected)
    query_source_connection_requests = select(UserBase, Connection.id, Connection.status).filter(
        Connection.source_user_id == id).where(
        Connection.target_user_id == UserType.id).where(Connection.status == ConnectionStatus.to_accept)
    connections_full_1 = session.execute(query_target_connections).fetchall()
    connections_full_2 = session.execute(query_source_connections).fetchall()
    connection_requests = session.execute(
        query_target_connection_requests).fetchall()
    connection_requests_sent = session.execute(
        query_source_connection_requests).fetchall()
    print(connections_full_1)
    return ConnectionResponseObj(connections=get_conn_list_from_rows([*connections_full_1, *connections_full_2]), connection_requests=get_conn_list_from_rows(connection_requests), connection_requests_sent=get_conn_list_from_rows(connection_requests_sent))


def get_user_connections(id: str):
    query_target_connections = select(UserBase, Connection.id, Connection.status).filter(
        Connection.target_user_id == id).where(UserType.id == Connection.source_user_id).where(Connection.status == ConnectionStatus.connected)
    query_source_connections = select(UserBase, Connection.id, Connection.status).filter(
        Connection.source_user_id == id).where(
        Connection.target_user_id == UserType.id).where(Connection.status == ConnectionStatus.connected)
    connections_full_1 = session.execute(query_target_connections).fetchall()
    connections_full_2 = session.execute(query_source_connections).fetchall()

    return ConnectionResponseObj(connections=get_conn_list_from_rows([*connections_full_1, *connections_full_2]))


def add_connection(source_user_id: str, target_user_id: str):
    user_source_present = session.execute(
        select(UserType.id).where(UserType.id == target_user_id)).scalar()
    user_target_present = session.execute(
        select(UserType.id).where(UserType.id == target_user_id)).scalar()

    if not user_source_present and not user_target_present:
        raise CustomException(message="No such user in DB")
    query = select(Connection.id).where(
        or_(and_(Connection.source_user_id == source_user_id, Connection.target_user_id == target_user_id), and_(Connection.source_user_id == target_user_id, Connection.target_user_id == source_user_id)))
    connection_exists = session.execute(query).scalar()

    if connection_exists:
        raise CustomException(message="Already connected!")

    connectioObj = Connection(source_user_id, target_user_id)
    session.add(connectioObj)
    session.commit()
    return True


def connection_action(connection_id: str, action: ConnectionAction) -> bool:
    status = session.execute(select(Connection.status).where(
        Connection.id == connection_id)).scalar()
    if status == ConnectionStatus.to_accept:
        if action == ConnectionAction.ACCEPT:
            session.execute(update(Connection).where(Connection.id ==
                                                     connection_id), {"status": ConnectionStatus.connected})
            session.commit()
        elif action == ConnectionAction.DECLINE:
            session.execute(delete(Connection).where(Connection.id ==
                                                     connection_id))
            session.commit()
        return True
    if status == ConnectionStatus.connected:
        session.execute(delete(Connection).where(Connection.id ==
                                                 connection_id))
        session.commit()
        return True
    return False
