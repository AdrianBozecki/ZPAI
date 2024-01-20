from sqlalchemy import select

from business_logic.entities.categories import CreateCategoryEntity, CategoryEntity
from business_logic.interfaces.categories import CategoryRepositoryInterface
from database import AsyncSessionLocal
from repositories.meals.models import Category


class CategoryRepository(CategoryRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def create_category(self, category: CreateCategoryEntity) -> Category:
        category = Category(**category.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def list_categories(self) -> list[Category]:
        results = await self.db.execute(select(Category))
        return results.scalars().all()
