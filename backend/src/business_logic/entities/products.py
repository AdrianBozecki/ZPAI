from pydantic import BaseModel

from enums import UnitOfMeasureEnum


class BaseProductEntity(BaseModel):
    value: float
    unit_of_measure: UnitOfMeasureEnum
    name: str


class CreateProductEntity(BaseProductEntity):
    pass


class ProductEntity(BaseProductEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True


class UpdateProductEntity(BaseModel):
    id: int
    value: float | None = None
    unit_of_measure: UnitOfMeasureEnum | None = None
    name: str | None = None