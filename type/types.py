import typing
import strawberry


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
