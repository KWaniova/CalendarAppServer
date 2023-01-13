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

    def __getitem__(self, index) -> EventModel:
        return self.get_by_id(index)
