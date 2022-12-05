from sqlalchemy.ext.declarative import declarative_base

from config import database

Base = declarative_base()

def create_all():
    Base.metadata.create_all(bind=database.current_database.engine)

class GenericBase(Base):
    __abstract__ = True
