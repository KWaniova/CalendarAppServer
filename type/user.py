from pydantic import BaseModel, validator
import strawberry
import re


@strawberry.input
class UserInput:
    first_name: str
    last_name: str
    email: str
    password: str


# TODO: how to do validation
# class User(BaseModel):
#     first_name: str
#     last_name: str
#     email: str
#     password: str

#     def __init__(self, user: UserInput) -> None:
#         self.first_name = user.first_name
#         self.last_name = user.last_name
#         self.email = user.email
#         self.password = user.password

#     @validator("email")
#     def check_email_format(cls, v):
#         regExs = r".*@.*/..*"
#         if not re.search(regExs[0], v):
#             return ValueError("email not match")
#         return v
