import typing
from models.index import Event as EventModel
from type.types import ResponseSuccess
from models.index import users, session


from sqlalchemy import *
from sqlalchemy.orm import *
import strawberry
from enum import Enum

import datetime
from models.event import events
from schemas.connection import get_user_connections

from type.types import EventsRepository


@strawberry.enum
class EventTypeEnum(Enum):
    PUBLIC = 3
    SHARED = 2
    PRIVATE = 1


@strawberry.input
class EventInput:
    title: str
    description: str
    start_date: str
    end_date: str


@strawberry.input
class EventInputUpdate:
    title: str
    description: str
    start_date: str
    end_date: str
    type: EventTypeEnum
    id: str


# PATTERN: Value object
@strawberry.type
class DateRange:
    start_date: datetime.datetime
    end_date: datetime.datetime


@strawberry.type
class Event:
    id: str
    title: str
    description: str
    type: EventTypeEnum
    date_range: DateRange
    user_id: str

    def __init__(self, id: str, title: str, description: str, type: EventTypeEnum, date_range: DateRange, user_id: str):
        self.id = id
        self.title = title
        self.description = description
        self.type = type
        self.date_range = date_range
        self.user_id = user_id


# PATTERN: Data Mapper
def map_event_to_event_model(instance: Event) -> EventModel:
    return EventModel(
        title=instance.title,
        description=instance.description,
        type=instance.type,
        start_date=instance.date_range.start_date,
        end_date=instance.date_range.end_date,
        user_id=instance.user_id
    )


def map_event_model_to_event(instance: EventModel) -> Event:
    return Event(
        id=instance.id,
        title=instance.title,
        description=instance.description,
        type=instance.type,
        date_range=DateRange(start_date=instance.start_date,
                             end_date=instance.end_date),
        user_id=instance.user_id
    )


REMOVED = object()


# PATTERN: Repository
class EventsRepository(EventsRepository):
    """EventsRepository"""

    def __init__(self, session: Session, identity_map=None):
        self.session = session
        self._identity_map = identity_map or dict()

    def add(self, entity: Event):
        self._identity_map[entity.id] = entity
        instance = map_event_to_event_model(entity)
        self.session.add(instance)

    def remove(self, entity: EventModel):
        self._check_not_removed(entity)
        self._identity_map[entity.id] = REMOVED
        listing_model = self.session.query(EventModel).get(entity.id)
        self.session.delete(listing_model)

    def update(self, entity: Event):
        self._check_not_removed(entity)
        result = session.execute(events.update().where(events.c.id == entity.id), {
            "title": entity.title,
            "description": entity.description,
            "type": entity.type,
            "start_date": entity.date_range.start_date,
            "end_date": entity.date_range.end_date
        })
        return result

    def get_by_id(self, id):
        instance = self.session.query(EventModel).get(id)
        return self._get_entity(instance, map_event_model_to_event)

    def get_by_user_id(self, user_id):
        instances = self.session.query(EventModel).filter(
            EventModel.user_id == user_id)
        return self._get_entities(instances, map_event_model_to_event)

    def get_by_user_id_and_date(self, user_id, date_range: DateRange):
        instances = self.session.query(EventModel).filter(
            EventModel.user_id == user_id).filter(EventModel.start_date >= date_range.start_date).filter(EventModel.end_date <= date_range.end_date)
        return self._get_entities(instances, map_event_model_to_event)

    def get_by_user_id_and_type(self, user_id, type: EventTypeEnum):
        instances = self.session.query(EventModel).filter(
            EventModel.user_id == user_id).filter(EventModel.type == type.value)
        return self._get_entities(instances, map_event_model_to_event)

    def _check_not_removed(self, entity):
        assert self._identity_map.get(
            entity.id, None) is not REMOVED, f"Entity {entity.id} already removed"

    def _get_entity(self, instance, mapper_func):
        if instance is None:
            return None
        entity = mapper_func(instance)
        self._check_not_removed(entity)

        if entity.id in self._identity_map:
            return self._identity_map[entity.id]

        self._identity_map[entity.id] = entity
        return entity

    def _get_entities(self, instances, mapper_func):
        entities = []
        for instance in instances:
            entity = self._get_entity(instance, mapper_func)
            entities.append(entity)
        return entities


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
    repository.add(event)
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
        repository.remove(event)
        session.commit()
        return True

    return False
