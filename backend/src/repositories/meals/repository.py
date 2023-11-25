from sqlalchemy.future import select

from business_logic.interfaces.meals import MealsRepositoryInterface
from database import AsyncSessionLocal
from repositories.meals.models import Meals


class MealsRepository(MealsRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def list_meals(self) -> list[Meals]:
        result = await self.db.execute(select(Meals))
        return result.scalars().all()
