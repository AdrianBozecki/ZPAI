from typing import Annotated

import pdfkit
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_restful.cbv import cbv
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.meals import CreateMealEntity, MealEntity, MealWithProductsEntity
from business_logic.use_cases.meals import CreateMealUseCase, ListMealsUseCase, DeleteMealUseCase, \
    GetShoppingListUseCase
from database import get_db
from repositories.meals import MealsRepository
meals_router = APIRouter()

@cbv(meals_router)
class MealsCBV:
    MEALS_BASE_URL = "/meals"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = MealsRepository(db)

    @meals_router.get(
        f"{MEALS_BASE_URL}",
        summary="List meals",
        response_description="Meals objects",
        status_code=status.HTTP_200_OK,
        response_model=list[MealEntity],
    )
    async def list_meals(self, category_id: int | None = None, name: str | None = None, ) -> list[MealEntity]:
        use_case = ListMealsUseCase(self.repo)
        meals = await use_case.execute(category_id, name)
        return meals

    @meals_router.post(
        f"{MEALS_BASE_URL}",
        summary="Create meal",
        response_description="Meal object",
        status_code=status.HTTP_201_CREATED,
        response_model=MealEntity,
    )
    async def create_meal(
        self,
        meal: CreateMealEntity = Body(..., description="Data for meal creation"),
    ) -> MealEntity:
        use_case = CreateMealUseCase(self.repo)
        return await use_case.execute(meal)


    @meals_router.delete(
        f"{MEALS_BASE_URL}/{{meal_id}}",
        summary="Delete meal",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_meal(self, meal_id: int) -> None:
        use_case = DeleteMealUseCase(self.repo)
        return await use_case.execute(meal_id)

    @meals_router.get(
        f"{MEALS_BASE_URL}/{{meal_id}}/shopping-list",
        summary="Get shopping list for meal",
        status_code=status.HTTP_200_OK,
    )
    async def get_shopping_list(self, meal_id: int) -> Response:
        use_case = GetShoppingListUseCase(self.repo)
        meal = await use_case.execute(meal_id)

        # Tworzenie struktury HTML dla pliku PDF
        html_content = f"<h1>Shopping list for: {meal.name}</h1><h2>Products:</h2><ul>"
        for product in meal.products:
            html_content += f"<li>{product.name}, {product.unit_of_measure}</li>"
        html_content += "</ul>"

        # Generowanie pliku PDF
        pdf_content = pdfkit.from_string(html_content, False)

        # Zwrócenie pliku PDF jako odpowiedzi na żądanie HTTP
        return Response(content=pdf_content, media_type="application/pdf")