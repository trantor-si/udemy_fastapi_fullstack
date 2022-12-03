from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from domain.models.generic import GenericBase


class UsersModel(GenericBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("TodosModel", back_populates="owner")
