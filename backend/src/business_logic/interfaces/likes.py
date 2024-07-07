from abc import ABC, abstractmethod

from business_logic.entities.likes import CreateLikeEntity


class LikesRepositoryInterface(ABC):
    @abstractmethod
    async def create_like(self, like: CreateLikeEntity) -> None:
        pass

    @abstractmethod
    async def delete_like(self, user_id: int, meal_id: int) -> None:
        pass
