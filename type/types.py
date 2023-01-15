import abc
import typing
import strawberry

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
# abstract base class for repository
class EventsRepository(metaclass=abc.ABCMeta):
    """An interface to listing repository"""

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
    def get_by_user_id(self, user_id):
        """Retrieves entity by user identity"""
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
