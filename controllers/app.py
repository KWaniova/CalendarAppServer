from fastapi import APIRouter

from schemas.schema import Mutation, Query
from strawberry.asgi import GraphQL
import strawberry


app_route = APIRouter()


schema = strawberry.Schema(
    query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

# app_route.add_route("/graphql", graphql_app)
