from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.schema import Mutation, Query
from strawberry.fastapi import GraphQLRouter
import strawberry

schema = strawberry.Schema(
    query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware, allow_headers=["*"], allow_origins=["http://127.0.0.1:8000/"], allow_origin_regex="https?://(localhost|127\.0\.0\.1):\d+."
# )

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(graphql_app, prefix="/graphql")


# app.include_router(app_route)
# app.add_websocket_route("/graphql", graphql_app)
