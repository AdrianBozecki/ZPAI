from business_logic.entities.comments import CreateCommentEntity, CommentEntity
from repositories.comment import CommentRepository


class CreateCommentUseCase:
    def __init__(self, comment_repo: CommentRepository):
        self.comment_repo = comment_repo

    async def execute(self, comment: CreateCommentEntity) -> CommentEntity:
        result = await self.comment_repo.create_comment(comment)
        return CommentEntity.from_orm(result)

class DeleteCommentUseCase:
    def __init__(self, comment_repo: CommentRepository):
        self.comment_repo = comment_repo

    async def execute(self, comment_id: int):
        await self.comment_repo.delete_comment(comment_id)


class ListCommentsUseCase:

    def __init__(self, comment_repo: CommentRepository):
        self.comment_repo = comment_repo

    async def execute(self, meal_id: int | None = None) -> list[CommentEntity]:
        comments = await self.comment_repo.list_comments(meal_id)
        return [CommentEntity.from_orm(comment) for comment in comments]