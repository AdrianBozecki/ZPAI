from business_logic.entities.categories import CategoryEntity, CreateCategoryEntity
from repositories.categories import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self, category: CreateCategoryEntity) -> CategoryEntity:
        result = await self.category_repo.create_category(category)
        return CategoryEntity.model_validate(result)

class ListCategoriesUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def execute(self) -> list[CategoryEntity]:
        result = await self.category_repo.list_categories()
        return [CategoryEntity.model_validate(category) for category in result]