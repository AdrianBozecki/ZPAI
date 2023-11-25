from abc import ABC, abstractmethod

from repositories.meals.models import Meals


class MealsRepositoryInterface(ABC):
    @abstractmethod
    async def list_meals(self) -> list[Meals]:
        pass
