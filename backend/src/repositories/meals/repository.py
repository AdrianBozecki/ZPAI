from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from business_logic.entities.meals import CreateMealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface
from database import AsyncSessionLocal
from repositories.meals.models import (
    Category,
    Meal,
    meal_category_association,
    meal_product_association,
)


class MealsRepository(MealsRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def list_meals(self, category_id: int | None) -> list[Meal]:
        query = select(Meal)
        if category_id is not None:
            query = query.join(Meal.category).filter(Category.id == category_id)
        query = query.options(joinedload(Meal.products), joinedload(Meal.category))

        result = await self.db.execute(query)

        meals = result.unique().scalars().all()
        return meals

    async def create_meal(self, meal: CreateMealEntity) -> Meal:
        new_meal = Meal(
            name=meal.name,
            description=meal.description,
            user_id=meal.user_id,
            likes_count=meal.likes_count,
            preparation=meal.preparation,
        )

        self.db.add(new_meal)
        await self.db.flush()

        for product_id in meal.product_ids:
            association = meal_product_association.insert().values(
                meal_id=new_meal.id,
                product_id=product_id,
            )
            await self.db.execute(association)

        for category_id in meal.category_ids:
            association = meal_category_association.insert().values(
                meal_id=new_meal.id,
                category_id=category_id,
            )
            await self.db.execute(association)

        await self.db.commit()

        await self.db.refresh(new_meal)
        refreshed_meal = await self.db.execute(
            select(Meal)
            .options(joinedload(Meal.products))
            .options(joinedload(Meal.category))
            .filter(Meal.id == new_meal.id),
        )
        return refreshed_meal.unique().scalars().one()
