from fastapi import APIRouter
from auth.typos import Request
from auth.users.retrieve_all.controller import RetrieveAllUsersController
from auth.users.shared.domain.users import User


router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/", response_model=list[User])
async def retrieve_all_users(request: Request):
    controller = RetrieveAllUsersController()
    return await controller.execute(request)
