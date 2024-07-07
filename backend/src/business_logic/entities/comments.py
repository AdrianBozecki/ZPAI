from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from repositories.models import Comment


class BaseCommentEntity(BaseModel):
    content: str
    meal_id: int

class CreateCommentEntity(BaseCommentEntity):
    user_id: int


class CommentUserEntity(BaseModel):
    id: int
    name: str
    lastname: str

class CommentEntity(BaseCommentEntity):
    id: int  # noqa: A003
    user: CommentUserEntity
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, comment: Comment) -> CommentEntity:
        return cls(
            id=comment.id,
            content=comment.content,
            meal_id=comment.meal_id,
            user=CommentUserEntity(id=comment.user_id, name=comment.user.user_details.name, lastname=comment.user.user_details.lastname),
            created_at=comment.created_at,
        )

