from fastapi import APIRouter, Body, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.likes import CreateLikeEntity
from business_logic.use_cases.likes import CreateLikeUseCase, DeleteLikeUseCase
from database import get_db
from repositories.likes import LikesRepository

likes_router = APIRouter()

@cbv(likes_router)
class LikesCBV:
    LIKES_BASE_URL = "/likes"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = LikesRepository(db)


    @likes_router.post(
        f"{LIKES_BASE_URL}",
        summary="Create like",
        response_description="No content",
        status_code=status.HTTP_201_CREATED,
        response_model=None,
    )
    async def create_like(
        self,
        like: CreateLikeEntity = Body(..., description="Data for like creation"),
    ) -> None:
        use_case = CreateLikeUseCase(self.repo)
        return await use_case.execute(like)

    @likes_router.delete(
        f"{LIKES_BASE_URL}/{{user_id}}/{{meal_id}}",
        summary="Delete like",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_like(self, user_id: int, meal_id: int) -> None:
        use_case = DeleteLikeUseCase(self.repo)
        return await use_case.execute(user_id, meal_id)

