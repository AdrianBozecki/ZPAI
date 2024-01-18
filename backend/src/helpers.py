import logging
from datetime import datetime, timedelta

from jose import jwt

from settings import settings

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_access_token(data: dict):
    logger.info(
        f"Czas wygaśnięcia tokena: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} {type(settings.ACCESS_TOKEN_EXPIRE_MINUTES)}"
    )
    logger.info(f"Klucz sekretny: {settings.SECRET_KEY}")
    logger.info(f"Algorytm: {settings.ALGORITHM}")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
