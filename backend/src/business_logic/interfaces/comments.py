from abc import ABC, abstractmethod

from business_logic.entities.comments import CreateCommentEntity
from repositories.models import Comment


class CommentRepositoryInterface(ABC):
    @abstractmethod
    async def create_comment(self, comment: CreateCommentEntity) -> Comment:
        pass


    @abstractmethod
    async def delete_comment(self, comment_id: int) -> None:
        pass

    @abstractmethod
    async def list_comments(self, meal_id: int | None = None) -> list[Comment]:
        pass