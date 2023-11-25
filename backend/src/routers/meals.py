from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.meals import MealEntity
from business_logic.use_cases.meals import ListMealsUseCase
from database import AsyncSessionLocal
from repositories.meals.repository import MealsRepository

meals_router = APIRouter()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@cbv(meals_router)
class MealsCBV:
    MEALS_BASE_URL = "/meals"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = MealsRepository(db)

    @meals_router.get(
        f"{MEALS_BASE_URL}/",
        summary="List meals",
        response_description="Meals objects",
        status_code=status.HTTP_200_OK,
        response_model=list[MealEntity],
    )
    async def list_meals(self) -> list[MealEntity]:
        use_case = ListMealsUseCase(self.repo)
        meals = await use_case.execute()
        return meals
