from abc import ABC, abstractmethod

from repositories.meals.models import Meal


class MealsRepositoryInterface(ABC):
    @abstractmethod
    async def list_meals(self) -> list[Meal]:
        pass
