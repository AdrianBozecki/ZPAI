from abc import ABC, abstractmethod

from business_logic.entities.products import CreateProductEntity
from repositories.models import Product


class ProductsRepositoryInterface(ABC):
    @abstractmethod
    async def create_product(self, product: CreateProductEntity) -> Product:
        pass
