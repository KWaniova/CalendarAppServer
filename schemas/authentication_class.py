import typing

from strawberry.permission import BasePermission
from strawberry.types import Info

from models.index import Token, session
from sqlalchemy import *


class IsAuthenticated(BasePermission):
    message = "User is not authenticated from IsAuthenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        print("Req: ", kwargs)

        if "auth" in kwargs.keys():
            isAuthorized = session.execute(select(Token.user_id).where(
                kwargs["auth"] == Token.token)).scalar()
            if isAuthorized:
                return True

        return False
