from decimal import Decimal as D
from typing import Annotated

from pydantic import BaseModel, Field


class BaseMealEntity(BaseModel):
    name: str
    description: str | None = None
    price: D
    user_id: int


class MealCreateEntity(BaseMealEntity):
    price: Annotated[D, Field(ge=0, decimal_places=2)]


class MealEntity(BaseMealEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True
