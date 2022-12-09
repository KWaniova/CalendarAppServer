from fastapi import APIRouter

from type.schema import Mutation, Query
from type.authorization import Mutation as AuthorizationMut, Query as AuthrorizationQuery
from strawberry.asgi import GraphQL
import strawberry
import typing

from functools import cached_property
from strawberry.fastapi import BaseContext, GraphQLRouter

user = APIRouter()


schema = strawberry.Schema(
    query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

user.add_route("/graphql", graphql_app)
