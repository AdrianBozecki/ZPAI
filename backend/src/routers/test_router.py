from fastapi import APIRouter

first_router = APIRouter()


@first_router.get("/test_router")
async def test_endpoint() -> dict[str, str]:
    return {"message": "Hello World"}
