from business_logic.entities.users import CreateUserEntity, UserEntity
from business_logic.interfaces.users import UsersRepositoryInterface
from database import AsyncSessionLocal
from repositories.meals.models import User, UserDetails


class UsersRepository(UsersRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def create_user(self, user: CreateUserEntity) -> UserEntity:
        user_details_row = UserDetails(
            name=user.name,
            lastname=user.lastname,
            phone_number=user.phone_number,
        )
        self.db.add(user_details_row)
        await self.db.flush()
        await self.db.refresh(user_details_row)

        user_row = User(
            email=user.email,
            password=user.password,
            user_details_id=user_details_row.id,
        )
        self.db.add(user_row)
        await self.db.commit()
        await self.db.refresh(user_row)

        return UserEntity(
            id=user_row.id,
            email=user_row.email,
            password=user_row.password,
            user_details_id=user_details_row.id,
            name=user_details_row.name,
            lastname=user_details_row.lastname,
            phone_number=user_details_row.phone_number,
        )
