from sqlalchemy.ext.declarative import declarative_base
from config.database import current_database

Base = declarative_base()
Base.metadata.create_all(bind=current_database.engine)

class GenericBase(Base):
    __abstract__ = True
