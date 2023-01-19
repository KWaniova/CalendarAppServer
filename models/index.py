from importlib.metadata import metadata
from models.user import users, User
from models.event import events, Event
from models.token import Token, auth_data
from models.connection import connections, Connection
from conn.db import Base, engine
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)
# PATTERN: Unit of work - vol2
session = Session(bind=engine)
