from fastapi import FastAPI

from routers.test_router import test_routero

app = FastAPI()

app.include_router(test_routero, tags=["test"])
