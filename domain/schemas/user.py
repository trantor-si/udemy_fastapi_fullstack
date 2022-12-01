from pydantic import Field

from domain.schemas.generic import GenericModel
from domain.schemas.item import Item


class UserBase(GenericModel):
    email: str = Field(title='User e-mail', example='user@domain.com')


class UserCreate(UserBase):
    password: str = Field(title='User password', example='pass123')


class User(UserBase):
    id: int = Field(title='User ID', example=12)
    is_active: bool = Field(title='User active status', example=True)
    items: list[Item] = Field(default=[], title='List of user items', example=[])

    class Config:
        orm_mode = True
