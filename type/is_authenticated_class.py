import typing

from strawberry.permission import BasePermission
from strawberry.types import Info

from type.authorization import authorized_user
from models.index import users, Token, session
from sqlalchemy import *


class IsAuthenticated(BasePermission):
    message = "User is not authenticated from IsAuthenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        print("REq: ", kwargs)

        if "auth" in kwargs.keys():
            isAuthorized = session.execute(select(Token.id_user).where(
                kwargs["auth"] == Token.token)).scalar()
            if isAuthorized:
                return True

        return False
