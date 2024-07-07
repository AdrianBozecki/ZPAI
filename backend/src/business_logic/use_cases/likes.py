

class CreateLikeUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, like) -> None:
        return await self.repo.create_like(like)

class DeleteLikeUseCase:

    def __init__(self, repo):
        self.repo = repo

    async def execute(self, user_id, meal_id) -> None:
        return await self.repo.delete_like(user_id, meal_id)
