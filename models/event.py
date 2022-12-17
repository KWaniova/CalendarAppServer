from conn.db import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer
from sqlalchemy.sql import func
import uuid
import enum
import strawberry
import datetime


@strawberry.enum
class EventType(enum.IntEnum):
    private = 1
    shared = 2
    public = 3


class Event(Base):
    __tablename__ = 'events'

    id = Column('id', String(40), primary_key=True)
    user_id = Column('user_id', ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    title = Column('title', String(
        60), nullable=False)
    description = Column('description', String(
        1000))
    type = Column('type', Integer, nullable=False)
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    created_at = Column(DateTime(), server_default=func.now())

    def __init__(self, user_id: str, title: str, description: str, start_date: datetime.datetime, end_date: datetime.datetime, type: int):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.description = description
        print("type: ", type)
        self.type = EventType.private.value if not type else type
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self) -> str:
        return f"({self.id}) {self.user_id} {self.title} {self.type} {self.created_at}"


events = Event.__table__
