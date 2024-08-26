from fastapi import APIRouter
from auth.typos import Request


router = APIRouter(
    tags=["ping"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ping")
async def ping(request: Request):
    request.app.logger.info("ping request")
    return "pong"
