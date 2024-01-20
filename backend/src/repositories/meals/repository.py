from sqlalchemy.future import select

from business_logic.entities.meals import CreateMealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface
from database import AsyncSessionLocal
from repositories.meals.models import Meal


class MealsRepository(MealsRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def list_meals(self) -> list[Meal]:
        result = await self.db.execute(select(Meal))
        return result.scalars().all()

    async def create_meal(self, meal: CreateMealEntity) -> Meal:
        meal = Meal(**meal.model_dump())
        self.db.add(meal)
        await self.db.commit()
        await self.db.refresh(meal)
        return meal
