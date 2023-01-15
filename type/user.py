from pydantic import BaseModel, validator
import strawberry
import re


@strawberry.input
class UserInput:
    first_name: str
    last_name: str
    email: str
    password: str
