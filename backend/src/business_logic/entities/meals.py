from pydantic import BaseModel


class MealCreateEntity(BaseModel):
    name: str
    description: str
    price: int
    user_id: int


class MealEntity(MealCreateEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True
