from conn.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String, DateTime
from sqlalchemy.sql import func
import uuid
from utils.hash_password import hash_password

from models.connection import connections


class User(Base):
    __tablename__ = 'users'

    id = Column('id', String(40), primary_key=True)
    first_name = Column('first_name', String(50))
    last_name = Column('last_name', String(50))
    email = Column('email', String(50), unique=True)
    password = Column('password', String(50))
    created_at = Column(DateTime(), server_default=func.now())

    def __init__(self, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = hash_password(password)
        print(hash_password(password) == self.password)

    def __repr__(self) -> str:
        return f"({self.id}) {self.first_name} {self.last_name} {self.email} {self.created_at}"


users = User.__table__
