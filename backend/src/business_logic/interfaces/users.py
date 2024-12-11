from abc import ABC, abstractmethod

from business_logic.entities.users import CreateUserEntity, UserEntity, UserLoginEntity


class UsersRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user: CreateUserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_user(self, user_email: str) -> UserEntity:
        pass

    @abstractmethod
    async def login_user(self, email: str, password: str) -> UserLoginEntity:
        pass

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> UserLoginEntity:
        pass