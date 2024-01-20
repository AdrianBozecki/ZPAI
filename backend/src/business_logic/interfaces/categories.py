from abc import ABC, abstractmethod

from business_logic.entities.categories import CategoryEntity, CreateCategoryEntity


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def create_category(self, category: CreateCategoryEntity) -> CategoryEntity:
        pass
