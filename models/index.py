from importlib.metadata import metadata
from models.user import users
from conn.db import Base, engine
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)
session = Session(bind=engine)
