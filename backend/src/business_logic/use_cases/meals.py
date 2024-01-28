from typing import List

from business_logic.entities.meals import CreateMealEntity, MealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface


class ListMealsUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, category_id: int | None, name: str | None) -> List[MealEntity]:
        meals = await self.repo.list_meals(category_id, name)
        return [MealEntity.from_orm(meal) for meal in meals]


class CreateMealUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal: CreateMealEntity) -> MealEntity:
        result = await self.repo.create_meal(meal)
        return MealEntity.from_orm(result)


class DeleteMealUseCase:

    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal_id: int) -> None:
        await self.repo.delete_meal(meal_id)
        return None
