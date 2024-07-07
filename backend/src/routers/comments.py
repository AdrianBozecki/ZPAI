from fastapi import APIRouter, Body, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.comments import CommentEntity, CreateCommentEntity
from business_logic.use_cases.comments import CreateCommentUseCase, DeleteCommentUseCase, \
    ListCommentsUseCase
from database import get_db
from repositories.comment import CommentRepository

comments_router = APIRouter()

@cbv(comments_router)
class CommentsCBV:
    COMMENTS_BASE_URL = "/comments"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = CommentRepository(db)


    @comments_router.post(
        f"{COMMENTS_BASE_URL}",
        summary="Create comment",
        response_description="Comment object",
        status_code=status.HTTP_201_CREATED,
        response_model=CommentEntity,
    )
    async def create_comment(
        self,
        comment: CreateCommentEntity = Body(..., description="Data for comment creation"),
    ) -> CommentEntity:
        use_case = CreateCommentUseCase(self.repo)
        return await use_case.execute(comment)


    @comments_router.delete(
        f"{COMMENTS_BASE_URL}/{{comment_id}}",
        summary="Delete comment",
        response_description="No content",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_comment(self, comment_id: int):
        use_case = DeleteCommentUseCase(self.repo)
        return await use_case.execute(comment_id)

    @comments_router.get(
        f"{COMMENTS_BASE_URL}",
        summary="List comments",
        response_description="Comments objects",
        status_code=status.HTTP_200_OK,
        response_model=list[CommentEntity],
    )
    async def list_comments(self, meal_id: int | None = None) -> list[CommentEntity]:
        use_case = ListCommentsUseCase(self.repo)
        comments = await use_case.execute(meal_id)
        return comments
