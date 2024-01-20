from pydantic import BaseModel


class BaseCategoryEntity(BaseModel):
    name: str


class CreateCategoryEntity(BaseCategoryEntity):
    pass


class CategoryEntity(BaseCategoryEntity):
    id: int  # noqa: A003

    class Config:
        from_attributes = True
