import logging
from typing import Annotated

import pdfkit
from fastapi import APIRouter, Body, Depends, UploadFile, File, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_restful.cbv import cbv
from fastapi.responses import Response
from pydantic import ValidationError, json
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.meals import CreateMealEntity, MealEntity, UpdateMealEntity
from business_logic.use_cases.meals import CreateMealUseCase, ListMealsUseCase, DeleteMealUseCase, \
    GetShoppingListUseCase, UpdateMealUseCase
from database import get_db
from enums import UnitSystemEnum
from repositories.meals import MealsRepository
from utils.minio_utils import upload_image

import json
from fastapi import HTTPException, Form


logger = logging.getLogger("foo-logger")
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
        response_description="No content",
        status_code=status.HTTP_201_CREATED,
        response_model=None,
    )
    async def create_meal(
            self,
            name: str = Form(...),
            description: str = Form(None),
            preparation: str = Form(None),
            user_id: int = Form(...),
            category_ids: str = Form(...),
            products: str = Form(...),
            image: UploadFile = File(None)
    ) -> None:
        try:
            category_ids_list = json.loads(category_ids)
            products_list = json.loads(products)
            meal_data = {
                "name": name,
                "description": description,
                "preparation": preparation,
                "user_id": user_id,
                "category_ids": category_ids_list,
                "products": products_list
            }
            meal_entity = CreateMealEntity(**meal_data)
        except (json.JSONDecodeError, ValidationError) as e:
            raise HTTPException(status_code=400, detail=str(e))

        logger.info(f"Creating meal: {meal_entity}")
        image_url = None
        if image:
            if image is not str:
                image_url = upload_image(image.file)
            else:
                image_url = image

        meal_entity.image_url = image_url
        logger.info(meal_entity.model_dump())
        use_case = CreateMealUseCase(self.repo)
        return await use_case.execute(meal_entity)


    @meals_router.delete(
        f"{MEALS_BASE_URL}/{{meal_id}}",
        summary="Delete meal",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_meal(self, meal_id: int) -> None:
        use_case = DeleteMealUseCase(self.repo)
        return await use_case.execute(meal_id)


    @meals_router.patch(
        f"{MEALS_BASE_URL}/{{meal_id}}",
        summary="Update meal",
        status_code=status.HTTP_200_OK,
        response_model=MealEntity,
    )
    async def update_meal(self, meal_id: int, meal: UpdateMealEntity = Body(..., description="Data for meal update")) -> MealEntity:
        use_case = UpdateMealUseCase(self.repo)
        meal.id = meal_id
        return await use_case.execute(meal)

    @meals_router.get(
        f"{MEALS_BASE_URL}/{{meal_id}}/shopping-list",
        summary="Get shopping list for meal",
        status_code=status.HTTP_200_OK,
    )
    async def get_shopping_list(self, meal_id: int, unit_system: UnitSystemEnum = UnitSystemEnum.METRIC) -> Response:
        use_case = GetShoppingListUseCase(self.repo)
        html_content = await use_case.execute(meal_id, unit_system)

        pdf_content = pdfkit.from_string(html_content, False)

        return Response(content=pdf_content, media_type="application/pdf")