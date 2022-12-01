from pydantic import Field

from domain.schemas.generic import GenericModel


class ItemBase(GenericModel):
    title: str = Field(title='Item title', example='item title')
    description: str | None = Field(
        default=None,
        title='Item description',
        example='item description',
    )


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int = Field(title='Item ID', example=101)
    owner_id: int = Field(title="Item's owner ID", example=63)

    class Config:
        orm_mode = True
