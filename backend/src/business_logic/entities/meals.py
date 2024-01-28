from __future__ import annotations

from pydantic import BaseModel, Field

from repositories.models import Meal


class BaseMealEntity(BaseModel):
    name: str
    description: str | None = None
    product_ids: list[int] = Field(default_factory=list)
    category_ids: list[int] = Field(default_factory=list)
    preparation: str | None = None
    user_id: int


class CreateMealEntity(BaseMealEntity):
    pass


class MealEntity(BaseMealEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, meal: Meal) -> MealEntity:
        return cls(
            id=meal.id,
            name=meal.name,
            description=meal.description,
            user_id=meal.user_id,
            product_ids=[product.id for product in meal.products],
            category_ids=[category.id for category in meal.category],
        )
