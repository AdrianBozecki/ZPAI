import logging
from typing import List

from business_logic.entities.meals import CreateMealEntity, MealEntity
from business_logic.interfaces.meals import MealsRepositoryInterface
from enums import UnitSystemEnum
from repositories.models import Meal
from utils.unit_converter import UnitConverter

logger = logging.getLogger("foo-logger")

class ListMealsUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, category_id: int | None, name: str | None) -> List[MealEntity]:
        meals = await self.repo.list_meals(category_id, name)
        return [MealEntity.from_orm(meal) for meal in meals]


class CreateMealUseCase:
    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal: CreateMealEntity) -> MealEntity:
        result = await self.repo.create_meal(meal)
        return MealEntity.from_orm(result)


class DeleteMealUseCase:

    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal_id: int) -> None:
        await self.repo.delete_meal(meal_id)
        return None


class GetShoppingListUseCase:

    def __init__(self, repo: MealsRepositoryInterface):
        self.repo = repo

    async def execute(self, meal_id: int, unit_system: UnitSystemEnum) -> str:
        results = await self.repo.get_meal(meal_id)
        meal_entity = MealEntity.from_orm(results)
        for product in meal_entity.products:
            product.value, product.unit_of_measure = UnitConverter.convert_unit(
                product.unit_of_measure, product.value, unit_system)

        return self.generate_pdf_content(meal_entity)

    def generate_pdf_content(self, meal: MealEntity) -> str:
        with open('utils/icon.html', 'r') as file:
            svg_content = file.read()

        html_content = f"<h1>Shopping list for: {meal.name}</h1>{svg_content}<h2>Products:</h2>"
        html_content += """
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 10px;
            }
        </style>
        <table>
          <tr>
            <th>Name</th>
            <th>Value</th>
            <th>Unit of Measure</th>
          </tr>
        """
        for product in meal.products:
            html_content += f"""
            <tr>
              <td>{product.name}</td>
              <td>{product.value}</td>
              <td>{product.unit_of_measure.value}</td>
            </tr>
            """
        html_content += "</table>"
        return html_content
