

from pydantic import BaseModel, Field



class BaseMealEntity(BaseModel):
    name: str
    description: str | None = None
    ingredients: list[str] = Field(default_factory=list)
    preparation: str | None = None
    user_id: int
    likes_count: int = 0


class CreateMealEntity(BaseMealEntity):
    pass


class MealEntity(BaseMealEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True
