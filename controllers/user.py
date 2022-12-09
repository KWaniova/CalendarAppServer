from fastapi import APIRouter

from type.user import Mutation, Query
from strawberry.asgi import GraphQL
import strawberry
import typing

from functools import cached_property
from strawberry.fastapi import BaseContext, GraphQLRouter

user = APIRouter()


schema = strawberry.Schema(Query, Mutation)
graphql_app = GraphQL(schema)

user.add_route("/graphql", graphql_app)
