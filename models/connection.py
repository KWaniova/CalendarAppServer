from conn.db import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer
from sqlalchemy.sql import func
import uuid
import enum


class ConnectionStatus(enum.IntEnum):
    to_accept = 1
    connected = 2


class Connection(Base):
    __tablename__ = 'connections'

    id = Column('id', String(40), primary_key=True)
    source_user_id = Column('source_user_id', ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    target_user_id = Column('target_user_id', ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    status = Column('status', Integer, nullable=False)
    created_at = Column(DateTime(), server_default=func.now())

    def __init__(self, source_user_id, target_user_id, status=None):
        self.id = str(uuid.uuid4())
        self.source_user_id = source_user_id
        self.target_user_id = target_user_id
        self.status = ConnectionStatus.to_accept.value if not status else ConnectionStatus[
            status]

    def __repr__(self) -> str:
        return f"({self.id}) {self.source_user_id} {self.target_user_id} {self.status} {self.created_at}"


connections = Connection.__table__
