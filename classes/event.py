from models.index import Event as EventModel
from models.index import users, session

from sqlalchemy import *
from sqlalchemy.orm import *
import strawberry
from enum import Enum

import datetime
from models.event import events
from type.types import BaseRepository, BaseMapper


@strawberry.enum
class EventTypeEnum(Enum):
    PUBLIC = 3
    SHARED = 2
    PRIVATE = 1


# PATTERN: Value object
@strawberry.type
class DateRange:
    start_date: datetime.datetime
    end_date: datetime.datetime


@strawberry.input
class DateRangeInput:
    start_date: datetime.datetime
    end_date: datetime.datetime


@strawberry.input
class EventInput:
    title: str
    description: str
    date_range: DateRangeInput


@strawberry.input
class EventInputUpdate:
    title: str
    description: str
    date_range: DateRangeInput
    type: EventTypeEnum
    id: str


# PATTERN: Embedded Value - DateRange
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
class EventMapper(BaseMapper):
    def map_to_entity(self, row: EventModel) -> Event:
        return Event(
            id=row.id,
            title=row.title,
            description=row.description,
            type=EventTypeEnum(row.type),
            date_range=DateRange(start_date=row.start_date,
                                 end_date=row.end_date),
            user_id=row.user_id
        )

    def map_to_model(self, instance: Event) -> Event:
        return EventModel(
            title=instance.title,
            description=instance.description,
            type=instance.type,
            start_date=instance.date_range.start_date,
            end_date=instance.date_range.end_date,
            user_id=instance.user_id
        )


REMOVED = object()


class EventsCriteriaMapper:
    def by_user_id(self, user_id):
        return select(EventModel).where(events.c.user_id == user_id)

    def get_by_user_id_and_date_range(self, user_id, date_range: DateRange):
        return select(EventModel).where(and_(events.c.user_id == user_id, events.c.start_date <= date_range.end_date, events.c.end_date >= date_range.start_date))

    def get_by_user_id_and_type(self, user_id, type: EventTypeEnum):
        return select(EventModel).where(and_(events.c.user_id == user_id, events.c.type == type.value))


# PATTERN: Repository


class EventsRepository(BaseRepository):
    """EventsRepository"""

    def __init__(self, session: Session, identity_map=None):
        self.session = session
        self.event_mapper = EventMapper()
        # PATTERN: Identity Map
        self._identity_map = identity_map or dict()

    def add(self, entity: Event):
        self._identity_map[entity.id] = entity
        instance = self.event_mapper.map_to_model(entity)
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
        self._identity_map[entity.id] = result
        return result

    def get_by_id(self, id):
        instance = self.session.query(EventModel).get(id)
        return self._get_entity(instance, self.event_mapper.map_to_entity)

    def matching(self, criteria):
        instances = session.scalars(criteria).all()
        return self._get_entities(instances, self.event_mapper.map_to_entity)

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
