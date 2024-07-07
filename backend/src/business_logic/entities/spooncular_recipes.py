from pydantic import BaseModel


class SpooncularIngredientsEntity(BaseModel):
    name: str
    unit: str
    amount: float

class SpooncularRecipeEntity(BaseModel):
    title: str
    image: str
    missed_ingredients: list[SpooncularIngredientsEntity]
    used_ingredients: list[SpooncularIngredientsEntity]
    instructions: str | None = None
    summary: str | None = None
