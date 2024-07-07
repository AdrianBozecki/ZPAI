import logging

from clients.base_http_client import BaseHTTPClient
from clients.converters import convert_from_json_to_entity
from settings import settings
logger = logging.getLogger("foo-logger")

class SpooncularAPIClient(BaseHTTPClient):
    def __init__(self):
        self.base_url = "https://api.spoonacular.com"
        self.headers = {"x-api-key": str(settings.SPOONCULAR_API_KEY)}
        super().__init__(self.base_url, self.headers)

    async def get_recipes_by_ingredients(self, ingredients: str):
        params = {"ingredients": ingredients, "number": 1}
        general_data = await self.make_request("/recipes/findByIngredients", params=params)
        general_data = general_data[0]
        additional_data = await self.make_request(f"/recipes/{general_data['id']}/information")
        return convert_from_json_to_entity(general_data, additional_data)
