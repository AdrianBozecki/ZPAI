import logging

from http_client.base_http_client import BaseHTTPClient
from http_client.converters import convert_from_json_to_entity
from settings import settings
logger = logging.getLogger("foo-logger")

class SpooncularAPIClient(BaseHTTPClient):
    def __init__(self):
        self.base_url = "https://api.spoonacular.com"
        self.headers = {"x-api-key": str(settings.SPOONCULAR_API_KEY)}
        super().__init__(self.base_url, self.headers)

    async def get_recipes_by_ingredients(self, ingredients: str):
        path = "/recipes/findByIngredients"
        params = {"ingredients": ingredients, "number": 1}
        result = await self.make_request(path, params=params)
        logger.debug(result)
        return convert_from_json_to_entity(result)
