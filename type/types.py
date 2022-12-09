import typing
import strawberry


T = typing.TypeVar("T")


@strawberry.type
class ResponseSuccess(typing.Generic[T]):
    status: int
    data: typing.Optional[T]
    message: str
