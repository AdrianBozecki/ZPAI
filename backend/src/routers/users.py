from fastapi import APIRouter, Body, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.users import CreateUserEntity, UserEntity, UserLoginEntity
from business_logic.use_cases.users import CreateUserUseCase, LoginUserUseCase
from database import get_db
from repositories.users import UsersRepository

users_router = APIRouter()


@cbv(users_router)
class UsersCBV:
    USERS_BASE_URL = "/users"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = UsersRepository(db)

    @users_router.post(
        f"{USERS_BASE_URL}/",
        summary="Create new user",
        response_description="User object",
        status_code=status.HTTP_201_CREATED,
        response_model=UserEntity,
    )
    async def create_user(
        self,
        item: CreateUserEntity = Body(..., description="Data for user creation"),
    ) -> UserEntity:
        use_case = CreateUserUseCase(self.repo)
        user = await use_case.execute(item)
        return user

    @users_router.post(
        f"{USERS_BASE_URL}/login/",
        summary="Login",
        response_description="User object",
        status_code=status.HTTP_200_OK,
        response_model=UserLoginEntity,
    )
    async def login(
        self,
        email: str = Body(..., description="User email"),
        password: str = Body(..., description="User password"),
    ) -> UserLoginEntity:
        use_case = LoginUserUseCase(self.repo)
        user = await use_case.execute(email, password)
        return user
