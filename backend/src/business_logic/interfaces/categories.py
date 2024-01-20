from abc import ABC, abstractmethod

from business_logic.entities.categories import CreateCategoryEntity
from repositories.meals.models import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def create_category(self, category: CreateCategoryEntity) -> Category:
        pass

    @abstractmethod
    async def list_categories(self) -> list[Category]:
        pass
