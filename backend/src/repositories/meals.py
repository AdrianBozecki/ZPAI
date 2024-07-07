import logging

from sqlalchemy import desc, delete
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from business_logic.entities.meals import CreateMealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface
from database import AsyncSessionLocal
from repositories.models import (
    Category,
    Meal,
    meal_category_association, Product,
)

logger = logging.getLogger("foo-logger")

class MealsRepository(MealsRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def get_meal(self, meal_id: int) -> Meal:
        query = select(Meal).options(selectinload(Meal.products), selectinload(Meal.category), selectinload(Meal.likes)).where(Meal.id == meal_id)
        result = await self.db.execute(query)
        meal = result.scalar_one_or_none()
        return meal

    async def list_meals(self, category_id: int | None, name: str | None) -> list[Meal]:
        query = select(Meal).order_by(desc(Meal.id))
        if category_id is not None:
            query = query.join(Meal.category).filter(Category.id == category_id)
        if name is not None:
            query = query.filter(Meal.name.ilike(f'%{name}%'))
        query = query.options(
            joinedload(Meal.category),
            joinedload(Meal.products),
            joinedload(Meal.likes),
        )
        result = await self.db.execute(query)

        meals = result.unique().scalars().all()
        return meals

    async def create_meal(self, meal: CreateMealEntity) -> Meal:
        new_meal = Meal(
            name=meal.name,
            description=meal.description,
            user_id=meal.user_id,
            preparation=meal.preparation,
        )

        self.db.add(new_meal)
        await self.db.flush()

        # Tworzenie produktów powiązanych z posiłkiem
        for product in meal.products:
            new_product = Product(
                name=product.name,
                unit_of_measure=product.unit_of_measure,
                value=product.value,
                meal_id=new_meal.id,
            )
            self.db.add(new_product)

        # Tworzenie powiązań z kategoriami
        for category_id in meal.category_ids:
            association = meal_category_association.insert().values(
                meal_id=new_meal.id,
                category_id=category_id,
            )
            await self.db.execute(association)

        await self.db.commit()

        # Odświeżanie danych posiłku po dodaniu produktów i powiązań z kategoriami
        await self.db.refresh(new_meal)
        refreshed_meal = await self.db.execute(
            select(Meal)
            .options(joinedload(Meal.products))
            .options(joinedload(Meal.category))
            .filter(Meal.id == new_meal.id),
        )
        return refreshed_meal.unique().scalars().one()

    async def delete_meal(self, meal_id: int) -> None:
        # Pobierz posiłek, który ma być usunięty
        result = await self.db.execute(select(Meal).where(Meal.id == meal_id))
        meal = result.scalar_one_or_none()

        if meal:
            # Usuń najpierw wszystkie powiązane produkty
            await self.db.execute(delete(Product).where(Product.meal_id == meal_id))

            # Teraz usuń posiłek
            await self.db.delete(meal)
            await self.db.commit()

        logger.info(f"Deleted meal: {meal}")
        return None