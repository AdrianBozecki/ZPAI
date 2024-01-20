from fastapi import APIRouter, Body, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.meals import CreateMealEntity, MealEntity
from business_logic.use_cases.meals import CreateMealUseCase, ListMealsUseCase
from database import get_db
from repositories.meals.repository import MealsRepository

meals_router = APIRouter()


@cbv(meals_router)
class MealsCBV:
    MEALS_BASE_URL = "/meals"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = MealsRepository(db)

    @meals_router.get(
        f"{MEALS_BASE_URL}",
        summary="List meals",
        response_description="Meals objects",
        status_code=status.HTTP_200_OK,
        response_model=list[MealEntity],
    )
    async def list_meals(self, category_id: int | None = None) -> list[MealEntity]:
        use_case = ListMealsUseCase(self.repo)
        meals = await use_case.execute(category_id)
        return meals

    @meals_router.post(
        f"{MEALS_BASE_URL}",
        summary="Create meal",
        response_description="Meal object",
        status_code=status.HTTP_201_CREATED,
        response_model=MealEntity,
    )
    async def create_meal(
        self,
        meal: CreateMealEntity = Body(..., description="Data for meal creation"),
    ) -> MealEntity:
        use_case = CreateMealUseCase(self.repo)
        return await use_case.execute(meal)
