from typing import List

from business_logic.entities.meals import MealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface


class ListMealsUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[MealEntity]:
        meals = await self.repo.list_meals()
        return [MealEntity.model_validate(meal) for meal in meals]
