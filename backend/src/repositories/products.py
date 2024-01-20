from business_logic.entities.products import CreateProductEntity
from business_logic.interfaces.products import ProductsRepositoryInterface
from database import AsyncSessionLocal
from repositories.models import Product


class ProductsRepository(ProductsRepositoryInterface):
    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def create_product(self, product: CreateProductEntity) -> Product:
        product = Product(**product.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
