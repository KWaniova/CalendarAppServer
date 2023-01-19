import abc
import typing
import strawberry

import sqlalchemy.orm as sa

from models.index import Event as EventModel


T = typing.TypeVar("T")


@strawberry.type
class ResponseSuccess(typing.Generic[T]):
    status: int
    data: typing.Optional[T]
    message: str


@strawberry.type
class Response(typing.Generic[T]):
    status: int
    data: T
    message: str


# PATTERN: SEPARATED INTERFACE
class BaseMapper:
    @abc.abstractmethod
    def map_to_model(self, row):
        raise NotImplementedError()

    def map_to_entity(self, entity):
        raise NotImplementedError()


class Resolver(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

# abstract base class for repository


class BaseRepository(metaclass=abc.ABCMeta):
    """An interface to listing repository"""
    session = sa.Session
    event_mapper = BaseMapper
    # PATTERN: Identity Map
    identity_map = {}

    @abc.abstractmethod
    def add(self, entity: EventModel):
        """Adds new entity to a repository"""
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: EventModel):
        """Removes existing entity from a repository"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(id: str) -> EventModel:
        """Retrieves entity by its identity"""
        raise NotImplementedError()

    @abc.abstractmethod
    def _check_not_removed(self, entity):
        """Checks if entity is removed"""
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_entity(self, instance, mapper_func):
        """Gets entity from instance"""
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_entities(self, instances, mapper_func):
        """Gets entities from instances"""
        raise NotImplementedError()
