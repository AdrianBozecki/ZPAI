from business_logic.entities.users import CreateUserEntity, UserEntity
from business_logic.interfaces.users import UsersRepositoryInterface


class CreateUserUseCase:
    def __init__(self, repo: UsersRepositoryInterface):
        self.repo = repo

    async def execute(self, user: CreateUserEntity) -> UserEntity:
        meals = await self.repo.create_user(user)
        return meals
