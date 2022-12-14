from fastapi import Request
from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult


from graphql.error.graphql_error import format_error as format_graphql_error


class CustomException(Exception):
    def __init__(self, message: str, status: int = None):
        self.message = message
        self.status = status


class UnauthorizedException(Exception):
    message = "Request not authorized!"
    status = 401


class MyGraphQLRouter(GraphQLRouter):

    async def process_result(
        self, request: Request, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        data: GraphQLHTTPResponse = {"data": result.data}

        if result.errors:
            data["errors"] = [format_graphql_error(
                err) for err in result.errors]

        return data
