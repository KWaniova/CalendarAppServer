from conn.db import Base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.sql import func
import uuid


class User(Base):
    __tablename__ = 'users'

    id = Column('id', String(40), primary_key=True)
    first_name = Column('first_name', String(50))
    last_name = Column('last_name', String(50))
    email = Column('email', String(50))
    password = Column('password', String(50))
    # created_at = Column(DateTime(), server_default=func.now())

    def __init__(self, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"({self.id}) {self.first_name} {self.last_name} {self.email}"


users = User.__table__
# users = Table('users', meta,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('first_name', String(50)),
#     Column('last_name', String(50)),
#     Column('email', String(50)),
#     Column('password', String(50)),
# )
