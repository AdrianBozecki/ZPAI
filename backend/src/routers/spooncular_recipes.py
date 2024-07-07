import logging

from fastapi import APIRouter, Query, Depends
from fastapi_restful.cbv import cbv

from business_logic.entities.spooncular_recipes import SpooncularRecipeEntity
from clients.http_client import SpooncularAPIClient

logger = logging.getLogger("foo-logger")

spooncular_meals_router = APIRouter()

def get_client() -> SpooncularAPIClient:
    return SpooncularAPIClient()

@cbv(spooncular_meals_router)
class SpooncularMealsCBV:
    SPOONCULAR_MEALS_BASE_URL = "/spooncular-meals"

    client: SpooncularAPIClient = Depends(get_client)

    @spooncular_meals_router.get(
        f"{SPOONCULAR_MEALS_BASE_URL}/find-by-ingredients/",
        summary="Get recipes by ingredients",
        response_description="Recipes objects",
        status_code=200,
        response_model=SpooncularRecipeEntity,
    )
    async def get_recipes_by_ingredients(self, ingredients: str = Query(..., description="Comma separated ingredients")) -> SpooncularRecipeEntity:
        response =  await self.client.get_recipes_by_ingredients(ingredients)
        return response
