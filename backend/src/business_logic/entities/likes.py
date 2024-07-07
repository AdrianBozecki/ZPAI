from pydantic import BaseModel


class BaseLikeEntity(BaseModel):
    user_id: int
    meal_id: int

class CreateLikeEntity(BaseLikeEntity):
    pass
