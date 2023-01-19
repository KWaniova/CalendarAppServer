import typing
from type.types import ResponseSuccess
from models.index import session

from sqlalchemy import *
from sqlalchemy.orm import *

import datetime
from schemas.connection_resolvers import ConnectionResolver

from classes.event import EventTypeEnum, EventInput, EventInputUpdate, DateRange, Event, EventsRepository, EventsCriteriaMapper
from type.types import Resolver


class EventResolver(Resolver):
    def __init__(self):
        self.repository = EventsRepository(session)
        self.conn_resolver = ConnectionResolver()
        pass

    def create_event(self, user_id: str, type: EventTypeEnum, event: EventInput) -> ResponseSuccess[str]:
        event = self._map_event_input_to_entity(event)
        event.user_id = user_id
        event.type = type.value
        self.repository.add(event)
        session.commit()
        return ResponseSuccess[None](status=201, message="created", data=event.id)

    def get_events_in_date_range(self, id: str, from_date: str, to_date: str) -> typing.List[Event]:
        date_range = DateRange(start_date=datetime.datetime.fromisoformat(
            from_date), end_date=datetime.datetime.fromisoformat(to_date))
        events_criteria_obj = EventsCriteriaMapper()
        criteria = events_criteria_obj.get_by_user_id_and_date_range(
            id, date_range)
        events = self.repository.matching(criteria)

        conn = self.conn_resolver.get_user_connections(id)
        for connection in conn.connections:
            connection_events_criteria = events_criteria_obj.get_by_user_id_and_type(
                connection.user_id, EventTypeEnum.PUBLIC)
            connection_events = self.repository.matching(
                connection_events_criteria)
            events.extend(connection_events)
        session.commit()

        return events

    def update_event(self, id: str, event_to_update: EventInputUpdate) -> ResponseSuccess[None]:
        event = self._map_event_input_to_entity(event_to_update)
        event.user_id = id
        event.type = event_to_update.type.value
        event.id = event_to_update.id
        self.repository.update(event)
        session.commit()
        return ResponseSuccess[None](status=201, message="Updated", data=None)

    def delete_event(self, user_id: str, id: str) -> bool:
        event = self.repository.get_by_id(id)
        if event and event.user_id == user_id:
            # PATTERN: Unit of work (session in SQLAlchemy)
            self.repository.remove(event)
            session.commit()
            return True

        return False

    def _map_event_input_to_entity(self, event: EventInput) -> Event:
        date_range = DateRange(
            start_date=event.date_range.start_date, end_date=event.date_range.end_date)
        event = Event(id=None, user_id=None, type=EventTypeEnum.PRIVATE.value, title=event.title,
                      description=event.description, date_range=date_range,)
        return event
