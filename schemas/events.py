import typing
import strawberry
from models.index import Event
from type.types import ResponseSuccess
from schemas.exceptions import CustomException
from models.index import users, session

from models.user import User as UserType


from sqlalchemy import *
from sqlalchemy.orm import *
from enum import Enum

from type.event import EventInput
import datetime


@strawberry.enum
class EventTypeEnum(Enum):
    PUBLIC = 3
    SHARED = 2
    PRIVATE = 1


def create_event(user_id: str, type: EventTypeEnum, event: EventInput, shared_with_ids: typing.Optional[typing.List[str]]):

    if EventTypeEnum.SHARED:
        # TODO: if time remains
        pass
    else:
        event = Event(user_id=user_id, type=type.value, title=event.title,
                      description=event.description, start_date=datetime.datetime.fromisoformat(event.start_date), end_date=datetime.datetime.fromisoformat(event.end_date))
        session.add(event)
        session.commit()
        pass


@strawberry.type
class MyEvent:
    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    type: EventTypeEnum


class EventMapper(Event):
    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    type: EventTypeEnum


def get_events_list_from_rows(rows) -> typing.List[MyEvent]:
    tab: typing.List[MyEvent] = []
    for row in rows:
        event: EventMapper = row[0]
        my_event = MyEvent(title=event.title, description=event.description,
                           type=event.type, start_date=event.start_date, end_date=event.end_date)
        tab.append(my_event)
    return tab


def get_my_events(id: str, from_date: str, to_date: str) -> typing.List[MyEvent]:
    query_events = session.query(Event).filter(
        Event.user_id == id).where(Event.user_id == UserType.id).where(
        Event.start_date >= datetime.datetime.fromisoformat(from_date)).where(Event.end_date <= datetime.datetime.fromisoformat(to_date))
    events = session.execute(
        query_events).fetchall()
    return get_events_list_from_rows(events)
