from abc import ABC, abstractmethod

from business_logic.entities.users import CreateUserEntity, UserEntity


class UsersRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user: CreateUserEntity) -> UserEntity:
        pass
