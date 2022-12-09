import typing
import strawberry


@strawberry.type
class ResponseSuccess:
    status: int
    data: typing.Optional[str]
    message: str
