from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///calendar_app_db.db', echo=True)
# meta = MetaData()
conn = engine.connect()
