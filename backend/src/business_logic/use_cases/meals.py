from typing import List

from business_logic.entities.meals import CreateMealEntity, MealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface


class ListMealsUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, category_id: int | None) -> List[MealEntity]:
        meals = await self.repo.list_meals(category_id)
        return [MealEntity.from_orm(meal) for meal in meals]


class CreateMealUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal: CreateMealEntity) -> MealEntity:
        result = await self.repo.create_meal(meal)
        return MealEntity.from_orm(result)
