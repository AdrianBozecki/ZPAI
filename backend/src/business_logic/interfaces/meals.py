from abc import ABC, abstractmethod

from business_logic.entities.meals import CreateMealEntity
from repositories.models import Meal


class MealsRepositoryInterface(ABC):
    @abstractmethod
    async def list_meals(self, category_id: int | None, name: str | None) -> list[Meal]:
        pass

    @abstractmethod
    async def create_meal(self, meal: CreateMealEntity) -> Meal:
        pass

    @abstractmethod
    async def delete_meal(self, meal_id: int) -> None:
        pass

    @abstractmethod
    async def get_meal(self, meal_id: int) -> Meal:
        pass

