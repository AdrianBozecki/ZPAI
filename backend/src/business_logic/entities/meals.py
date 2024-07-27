from __future__ import annotations

import logging

from pydantic import BaseModel, Field

from business_logic.entities.products import ProductEntity, CreateProductEntity, UpdateProductEntity
from repositories.models import Meal
logger = logging.getLogger("foo-logger")


class BaseMealEntity(BaseModel):
    name: str
    description: str | None = None
    category_ids: list[int] = Field(default_factory=list)
    preparation: str | None = None
    user_id: int

class CreateMealEntity(BaseMealEntity):
    products: list[CreateProductEntity] = Field(default_factory=list)

class MealEntity(BaseMealEntity):
    id: int  # noqa: A003
    products: list[ProductEntity] = Field(default_factory=list)
    likes_count: int = 0

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, meal: Meal) -> MealEntity:
        return cls(
            id=meal.id,
            name=meal.name,
            description=meal.description,
            preparation=meal.preparation,
            user_id=meal.user_id,
            products=meal.products,
            category_ids=[category.id for category in meal.category],
            likes_count=len(meal.likes),
        )




class UpdateMealEntity(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    preparation: str | None = None
    products: list[UpdateProductEntity] | None = None
    category_ids: list[int] | None = None

