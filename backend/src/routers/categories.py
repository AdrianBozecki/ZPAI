from fastapi import APIRouter, Depends, Body
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.categories import CategoryEntity, CreateCategoryEntity
from business_logic.entities.meals import MealEntity, CreateMealEntity
from business_logic.use_cases.categories import CreateCategoryUseCase
from business_logic.use_cases.meals import ListMealsUseCase, CreateMealUseCase
from database import get_db
from repositories.categories import CategoryRepository
from repositories.meals.repository import MealsRepository

categories_router = APIRouter()


@cbv(categories_router)
class CategoriesCBV:
    CATEGORIES_BASE_URL = "/categories"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = CategoryRepository(db)


    @categories_router.post(
        f"{CATEGORIES_BASE_URL}",
        summary="Create category",
        response_description="Category object",
        status_code=status.HTTP_201_CREATED,
        response_model=CategoryEntity,
    )
    async def create_category(
            self,
            category: CreateCategoryEntity = Body(..., description="Data for category creation"),
    ) -> CategoryEntity:
        use_case = CreateCategoryUseCase(self.repo)
        return await use_case.execute(category)

