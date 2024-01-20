from pydantic import BaseModel

from enums import UnitOfMeasureEnum


class BaseProductEntity(BaseModel):
    name: str
    unit_of_measure: UnitOfMeasureEnum | None = None


class CreateProductEntity(BaseProductEntity):
    pass


class ProductEntity(BaseProductEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True
