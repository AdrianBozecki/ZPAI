import bcrypt
from fastapi import HTTPException
from sqlalchemy import select

from business_logic.entities.users import CreateUserEntity, UserEntity, UserLoginEntity
from business_logic.interfaces.users import UsersRepositoryInterface
from consts import BEARER
from database import AsyncSessionLocal
from helpers import create_access_token
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

        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        user_row = User(
            email=user.email,
            password=hashed_password.decode("utf-8"),
            user_details_id=user_details_row.id,
        )
        self.db.add(user_row)
        await self.db.commit()
        await self.db.refresh(user_row)

        return UserEntity(
            id=user_row.id,
            email=user_row.email,
            user_details_id=user_details_row.id,
            name=user_details_row.name,
            lastname=user_details_row.lastname,
            phone_number=user_details_row.phone_number,
        )

    async def get_user(self, user_email: str) -> UserEntity:
        query = select(User, UserDetails).join(UserDetails).where(User.email == user_email)
        user_row, user_details_row = (await self.db.execute(query)).first()

        return UserEntity(
            id=user_row.id,
            email=user_row.email,
            user_details_id=user_details_row.id,
            name=user_details_row.name,
            lastname=user_details_row.lastname,
            phone_number=user_details_row.phone_number,
        )

    async def login_user(self, email: str, password: str) -> UserLoginEntity:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user_row = result.scalar_one_or_none()

        if user_row is None:
            raise HTTPException(status_code=401, detail="User not found")

        if not bcrypt.checkpw(password.encode("utf-8"), user_row.password.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Incorrect password")

        access_token = create_access_token(data={"sub": user_row.email})

        return UserLoginEntity(
            access_token=access_token,
            token_type=BEARER,
        )
