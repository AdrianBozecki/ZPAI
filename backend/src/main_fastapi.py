from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from business_logic.use_cases.users import GetUserUseCase
from database import Base, engine, get_db_for_middleware
from repositories.meals.models import User
from repositories.users.repository import UsersRepository
from routers.meals import meals_router
from routers.test_router import first_router
from routers.users import users_router
from settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(first_router, tags=["test"])
app.include_router(meals_router, tags=["meals"])
app.include_router(users_router, tags=["users"])


@app.on_event("startup")
async def startup_event() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    request.state.user = None
    token = request.headers.get('authorization')

    if request.url.path not in ['/users/login/', '/users/']:
        if token is not None:
            token = token.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                email: str = payload.get("sub")

                if email is None:
                    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

                async with get_db_for_middleware() as db:
                    user_repo = UsersRepository(db)
                    use_case = GetUserUseCase(user_repo)
                    user = await use_case.execute(email)

                request.state.user = user

            except JWTError:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing authorization header")

    response = await call_next(request)
    return response