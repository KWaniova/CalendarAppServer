import typing
from type.types import ResponseSuccess
from models.index import users, session

from sqlalchemy import *
from sqlalchemy.orm import *

import datetime
from schemas.connection import get_user_connections

from classes.event import EventTypeEnum, EventInput, EventInputUpdate, DateRange, Event, EventsRepository


def map_event_input_to_entity(event: EventInput) -> Event:
    date_range = DateRange(start_date=datetime.datetime.fromisoformat(
        event.start_date), end_date=datetime.datetime.fromisoformat(event.end_date))
    event = Event(id=None, user_id=None, type=EventTypeEnum.PRIVATE.value, title=event.title,
                  description=event.description, date_range=date_range,)
    return event


def create_event(user_id: str, type: EventTypeEnum, event: EventInput) -> ResponseSuccess[str]:
    event = map_event_input_to_entity(event)
    event.user_id = user_id
    event.type = type.value

    repository = EventsRepository(session)
    # print("Identity set 1: ", session.new)
    repository.add(event)
    # print("Identity set 2: ", session.new)
    session.commit()
    return ResponseSuccess[None](status=201, message="created", data=event.id)


def get_my_events(id: str, from_date: str, to_date: str) -> typing.List[Event]:
    repository = EventsRepository(session)
    date_range = DateRange(start_date=datetime.datetime.fromisoformat(
        from_date), end_date=datetime.datetime.fromisoformat(to_date))
    events = repository.get_by_user_id_and_date(id, date_range)
    conn = get_user_connections(id)
    for connection in conn.connections:
        connection_events = repository.get_by_user_id_and_type(
            connection.user_id, EventTypeEnum.PUBLIC)
        events.extend(connection_events)
    session.commit()

    return events


def update_event(id: str, event_to_update: EventInputUpdate) -> ResponseSuccess[None]:
    event = map_event_input_to_entity(event_to_update)
    event.user_id = id
    event.type = event_to_update.type.value
    event.id = event_to_update.id
    repository = EventsRepository(session)
    repository.update(event)
    session.commit()
    return ResponseSuccess[None](status=201, message="Updated", data=None)


def delete_event(user_id: str, id: str) -> bool:
    repository = EventsRepository(session)
    event = repository.get_by_id(id)
    if event and event.user_id == user_id:
        # PATTERN: Unit of work (session in SQLAlchemy)
        repository.remove(event)
        session.commit()
        return True

    return False
