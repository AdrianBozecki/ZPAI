from abc import ABC, abstractmethod

from business_logic.entities.categories import CategoryEntity, CreateCategoryEntity
from business_logic.entities.products import CreateProductEntity, ProductEntity
from repositories.meals.models import Product


class ProductsRepositoryInterface(ABC):
    @abstractmethod
    async def create_product(self, product: CreateProductEntity) -> Product:
        pass
