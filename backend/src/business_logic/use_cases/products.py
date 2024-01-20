from business_logic.entities.products import CreateProductEntity, ProductEntity
from business_logic.interfaces.products import ProductsRepositoryInterface


class CreateProductUseCase:
    def __init__(self, repo: ProductsRepositoryInterface):
        self.repo = repo

    async def execute(self, product: CreateProductEntity) -> ProductEntity:
        result = await self.repo.create_product(product)
        return ProductEntity.model_validate(result)
