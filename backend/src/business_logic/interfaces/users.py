from abc import ABC, abstractmethod

from business_logic.entities.users import CreateUserEntity, UserEntity


class UsersRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user: CreateUserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> UserEntity:
        pass

    @abstractmethod
    async def login_user(self, email: str, password: str) -> UserEntity:
        pass