import logging

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from business_logic.entities.comments import CreateCommentEntity
from business_logic.interfaces.comments import CommentRepositoryInterface
from database import AsyncSessionLocal
from repositories.models import Comment, User
logger = logging.getLogger("foo-logger")

class CommentRepository(CommentRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def create_comment(self, comment: CreateCommentEntity) -> Comment:
        comment = Comment(**comment.model_dump())
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)

        query = select(Comment).options(joinedload(Comment.user).joinedload(User.user_details)).where(Comment.id == comment.id)
        result = await self.db.execute(query)
        comment_with_user = result.scalar_one_or_none()
        return comment_with_user


    async def delete_comment(self, comment_id: int) -> None:
        comment = await self.db.execute(select(Comment).filter(Comment.id == comment_id))
        self.db.delete(comment)
        await self.db.commit()

    async def list_comments(self, meal_id: int | None = None) -> list[Comment]:
        query = select(Comment).options(joinedload(Comment.user).joinedload(User.user_details))
        if meal_id is not None:
            query = query.where(Comment.meal_id == meal_id)
        result = await self.db.execute(query)
        comments = result.scalars().all()
        return comments
