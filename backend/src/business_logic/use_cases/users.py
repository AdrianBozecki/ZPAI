from business_logic.entities.users import CreateUserEntity, UserEntity
from business_logic.interfaces.users import UsersRepositoryInterface


class CreateUserUseCase:
    def __init__(self, repo: UsersRepositoryInterface):
        self.repo = repo

    async def execute(self, user: CreateUserEntity) -> UserEntity:
        meals = await self.repo.create_user(user)
        return meals


class GetUserUseCase:
    def __init__(self, repo: UsersRepositoryInterface):
        self.repo = repo

    async def execute(self, user_id: int) -> UserEntity:
        meals = await self.repo.get_user(user_id)
        return meals


class LoginUserUseCase:
    def __init__(self, repo: UsersRepositoryInterface):
        self.repo = repo

    async def execute(self, email: str, password: str) -> UserEntity | None:
        meals = await self.repo.login_user(email, password)
        return meals
