from conn.db import Base
from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import String
from utils.get_token_string import get_token_string
from sqlalchemy import ForeignKey
from models.index import User


class Token(Base):
    __tablename__ = 'auth_data'

    id_user = Column('id_user', ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    token = Column('token', String(40), primary_key=True)

    def __init__(self, id: str, password: str):
        self.id_user = id
        self.token = get_token_string(password, id)

    def __repr__(self) -> str:
        return f"({self.id_user}) {self.token}"


auth_data = User.__table__
