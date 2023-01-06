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
from models.event import events
from schemas.connection import get_user_connections


@strawberry.enum
class EventTypeEnum(Enum):
    PUBLIC = 3
    SHARED = 2
    PRIVATE = 1


@strawberry.input
class EventInputUpdate:
    title: str
    description: str
    start_date: str
    end_date: str
    type: EventTypeEnum
    id: str


def create_event(user_id: str, type: EventTypeEnum, event: EventInput) -> ResponseSuccess[str]:

    if type == EventTypeEnum.SHARED:
        # TODO: if time remains
        return ResponseSuccess[None](status=201, message="created", data=None)

    event = Event(user_id=user_id, type=type.value, title=event.title,
                  description=event.description, start_date=datetime.datetime.fromisoformat(event.start_date), end_date=datetime.datetime.fromisoformat(event.end_date))
    session.add(event)
    session.commit()
    return ResponseSuccess[None](status=201, message="created", data=event.id)


@strawberry.type
class MyEvent:
    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    type: EventTypeEnum
    user_id: str
    id: str


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
        print("EVENT ", event)
        my_event = MyEvent(id=event.id, user_id=event.user_id, title=event.title, description=event.description,
                           type=event.type, start_date=event.start_date, end_date=event.end_date)
        tab.append(my_event)
    return tab


def get_my_events(id: str, from_date: str, to_date: str) -> typing.List[MyEvent]:
    query_events = session.query(Event).filter(
        Event.user_id == id).where(Event.user_id == UserType.id).filter(or_(Event.start_date >= datetime.datetime.fromisoformat(from_date), Event.end_date <= datetime.datetime.fromisoformat(to_date)))
    events = session.execute(
        query_events).fetchall()
    conn = get_user_connections(id)
    for connection in conn.connections:
        connection_events = session.execute(session.query(Event).filter(
            Event.user_id == connection.user_id).filter(Event.type == EventTypeEnum.PUBLIC.value)).fetchall()
        print("connection_events: ", connection_events)
        events.extend(connection_events)
    return get_events_list_from_rows(events)


def update_event(id: str, event: EventInputUpdate) -> ResponseSuccess[None]:
    eventResult = session.execute(select(Event).where(
        Event.id == event.id)).fetchall()
    print("UPDATE: ", eventResult)

    result = session.execute(events.update().where(events.c.id == event.id), {
        "title": event.title,
        "description": event.description,
        "type": event.type.value,
        "start_date": datetime.datetime.fromisoformat(event.start_date),
        "end_date": datetime.datetime.fromisoformat(event.end_date)
    })
    return ResponseSuccess[None](status=201, message=str(result.rowcount) + " Row(s) updated", data=None)


def delete_event(user_id: str, id: str) -> bool:
    event = session.execute(
        events.select().where(events.c.id == id)).fetchone()
    print("EEVV: ", event)
    if event and event.user_id == user_id:
        result = session.execute(events.delete().where(events.c.id == id))
        return result.rowcount > 0
    return False

# TODO: where with condition or - because not returning some events
