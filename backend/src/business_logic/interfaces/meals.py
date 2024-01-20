from abc import ABC, abstractmethod

from business_logic.entities.meals import CreateMealEntity
from repositories.meals.models import Meal


class MealsRepositoryInterface(ABC):
    @abstractmethod
    async def list_meals(self, category_id: int | None) -> list[Meal]:
        pass

    @abstractmethod
    async def create_meal(self, meal: CreateMealEntity) -> Meal:
        pass
