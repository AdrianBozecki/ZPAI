from typing import List

from business_logic.entities.meals import MealEntity, CreateMealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface


class ListMealsUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[MealEntity]:
        meals = await self.repo.list_meals()
        return [MealEntity.from_orm(meal) for meal in meals]


class CreateMealUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal: CreateMealEntity) -> MealEntity:
        result = await self.repo.create_meal(meal)
        return MealEntity.model_validate(result)