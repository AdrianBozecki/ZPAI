from fastapi import APIRouter

test_routero = APIRouter()


@test_routero.get("/test_router/")
async def test_endpoint() -> dict[str, str]:
    return {"message": "Hello World Dupa"}
