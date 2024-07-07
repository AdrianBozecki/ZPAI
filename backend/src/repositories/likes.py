
from sqlalchemy.future import select

from business_logic.entities.likes import CreateLikeEntity
from business_logic.interfaces.likes import LikesRepositoryInterface
from database import AsyncSessionLocal
from repositories.models import Like
class LikesRepository(LikesRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def create_like(self, like: CreateLikeEntity) -> None:
        like = Like(**like.model_dump())
        self.db.add(like)
        await self.db.commit()
        return None

    async def delete_like(self, user_id: int, meal_id: int) -> None:
        result = await self.db.execute(
            select(Like).filter(Like.user_id == user_id, Like.meal_id == meal_id))
        like = result.scalar_one_or_none()
        if like is not None:
            await self.db.delete(like)  # Dodaj await tutaj
            await self.db.commit()
        return None