from datetime import datetime

import bcrypt
from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy import select

from business_logic.entities.users import CreateUserEntity, UserEntity, UserLoginEntity
from business_logic.interfaces.users import UsersRepositoryInterface
from consts import BEARER
from database import AsyncSessionLocal
from helpers import create_access_token, create_refresh_token
from repositories.models import User, UserDetails, RefreshToken
from settings import settings


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

        if user_row is None:
            raise HTTPException(status_code=401, detail="User not found")

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
        refresh_token = create_refresh_token(data={"sub": user_row.email})

        old_refresh_token_query = select(RefreshToken).where(RefreshToken.user_email == user_row.email)
        result = await self.db.execute(old_refresh_token_query)
        old_refresh_token = result.scalar_one_or_none()
        await self.db.delete(old_refresh_token)

        # Save the refresh token to the database
        refresh_token_row = RefreshToken(
            token=refresh_token,
            user_email=user_row.email,
        )
        self.db.add(refresh_token_row)
        await self.db.commit()
        await self.db.refresh(refresh_token_row)

        return UserLoginEntity(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=BEARER,
            user_id=user_row.id,
        )

    async def refresh_token(self, refresh_token: str) -> UserLoginEntity:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            user_email: str = payload.get("sub")
            if user_email is None:
                raise HTTPException(status_code=401, detail="Invalid token")

            query = await self.db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token,
                                                                RefreshToken.user_email == user_email))
            db_refresh_token = query.scalar_one_or_none()
            if db_refresh_token is None or db_refresh_token.expires_at < datetime.now():
                raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

            user = await self.get_user(user_email)
            new_access_token = create_access_token(data={"sub": user_email})
            return UserLoginEntity(
                access_token=new_access_token,
                refresh_token=refresh_token,
                token_type=BEARER,
                user_id=user.id,
            )

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
