from fastapi import APIRouter

from type.schema import Mutation, Query
from strawberry.asgi import GraphQL
import strawberry


user = APIRouter()


schema = strawberry.Schema(
    query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

user.add_route("/graphql", graphql_app)
