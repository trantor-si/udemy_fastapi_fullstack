from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DBConnection

load_dotenv()

class Database:
  def __init__(self, type : str = None):
    self.type = type
    self.db_connection = DBConnection(self.type)
    self.engine = self.get_engine()

  def get_engine(self):
    self.engine = None
    self.url = self.db_connection.get_url()
    self.connect_args = self.db_connection.get_connect_args()

    if self.connect_args is None:
      self.engine = create_engine(self.url)
    else:
      print(self.url, self.connect_args)
      self.engine = create_engine(self.url, connect_args={"check_same_thread": False})

    if self.engine is not None:
      self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
      self.Base = declarative_base()
    else:
      raise Exception('Error creating engine for database type: [{}].'.format(self.db_connection.get_type()))

    return self.engine

# define the current database 
def new_database(type : str = None):
  global current_database
  current_database = Database(type)

def get_session():
  try:
      current_database.session = current_database.SessionLocal()
      yield current_database.session
  finally:
      current_database.session.close()
