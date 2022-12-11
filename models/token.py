from conn.db import Base
from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import String
from utils.get_token_string import get_token_string
from sqlalchemy import ForeignKey
from models.index import User


class Token(Base):
    __tablename__ = 'auth_data'

    user_id = Column('user_id', ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    token = Column('token', String(40), primary_key=True)

    def __init__(self, id: str, password: str):
        self.user_id = id
        self.token = get_token_string(password, id)

    def __repr__(self) -> str:
        return f"({self.user_id}) {self.token}"


auth_data = User.__table__
