import os
from typing import Any

from pydantic import BaseModel


class Settings(BaseModel):
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    ALGORITHM: str | None = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    LOG_CONFIG: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "foo-logger": {"handlers": ["default"], "level": "DEBUG"},
        },
    }
    SPOONCULAR_API_KEY: str | None = os.getenv("SPOONCULAR_API_KEY")


settings = Settings()
