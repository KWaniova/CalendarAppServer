from importlib.metadata import metadata
from models.user import users, User
from models.token import Token, auth_data
from conn.db import Base, engine
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)
session = Session(bind=engine)
