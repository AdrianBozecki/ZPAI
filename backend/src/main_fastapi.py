import logging
from logging.config import dictConfig

from fastapi import FastAPI, Security, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_401_UNAUTHORIZED

from business_logic.use_cases.users import GetUserUseCase
from database import Base, engine, get_db_for_middleware
from repositories.users import UsersRepository
from routers.categories import categories_router
from routers.meals import meals_router
from routers.products import products_router
from routers.users import users_router
from settings import settings
import pdfkit

dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("foo-logger")

app = FastAPI(debug=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meals_router, tags=["meals"])
app.include_router(users_router, tags=["users"])
app.include_router(categories_router, tags=["categories"])
app.include_router(products_router, tags=["products"])


@app.on_event("startup")
async def startup_event() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# @app.middleware("http")
# async def jwt_middleware(
#     request: Request,
#     call_next: RequestResponseEndpoint,
# ) -> JSONResponse | Response:
#     if request.method == "OPTIONS":
#         return await call_next(request)
#
#     request.state.user = None
#     token = request.headers.get("authorization")
#     logger.debug(request.headers)
#     if request.url.path not in ["/users/login/", "/users/", "/docs", "/openapi.json"]:
#         if token is not None:
#             token = token.split(" ")[1]
#             try:
#                 payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#                 email: str = payload.get("sub")
#
#                 if email is None:
#                     return JSONResponse(
#                         status_code=HTTP_401_UNAUTHORIZED,
#                         content={"detail": "Invalid token"},
#                     )
#
#                 async with get_db_for_middleware() as db:
#                     user_repo = UsersRepository(db)
#                     use_case = GetUserUseCase(user_repo)
#                     user = await use_case.execute(email)
#
#                     if user.id != int(request.headers.get("user_id")):
#                         return JSONResponse(
#                             status_code=HTTP_401_UNAUTHORIZED,
#                             content={"detail": request.headers.get("user_id")},
#                         )
#
#                 request.state.user = user
#
#             except JWTError:
#                 return JSONResponse(
#                     status_code=HTTP_401_UNAUTHORIZED,
#                     content={"detail": "Invalid token"},
#                 )
#         else:
#             return JSONResponse(
#                 status_code=HTTP_401_UNAUTHORIZED,
#                 content={"detail": "Missing authorization header"},
#             )
#
#     response = await call_next(request)
#     return response
