from fastapi import APIRouter, Body, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from business_logic.entities.products import CreateProductEntity, ProductEntity
from business_logic.use_cases.products import CreateProductUseCase
from database import get_db
from repositories.products import ProductsRepository

products_router = APIRouter()


@cbv(products_router)
class ProductsCBV:
    PRODUCTS_BASE_URL = "/products"

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = ProductsRepository(db)

    @products_router.post(
        f"{PRODUCTS_BASE_URL}",
        summary="Create product",
        response_description="Product object",
        status_code=status.HTTP_201_CREATED,
        response_model=ProductEntity,
    )
    async def create_product(
        self,
        product: CreateProductEntity = Body(..., description="Data for product creation"),
    ) -> ProductEntity:
        use_case = CreateProductUseCase(self.repo)
        return await use_case.execute(product)
