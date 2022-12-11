import typing
import strawberry
from conn.db import conn, engine
from models.index import connections, session, Connection
from models.user import User as UserType
from type.types import ResponseSuccess
from type.exceptions import CustomException

from sqlalchemy import *
from sqlalchemy.orm import *


@strawberry.type
class ConnectionBase(UserType):
    id: str
    first_name: str
    last_name: str


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


def get_my_connections(id) -> typing.Optional[typing.List[ConnectionBase]]:
    query_target = select(ConnectionBase).filter(
        Connection.source_user_id == id).where(UserType.id == Connection.target_user_id)
    query_source = select(Connection.source_user_id).where(
        Connection.target_user_id == id)
    conn = session.execute(query_target).fetchall()
    tab = []
    for row in conn:
        tab.append(row[0])
    return tab


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
