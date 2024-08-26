from auth.typos import Request
from auth.users.retrieve_all.retriever import AllUsersRetriever
from auth.users.shared.infrastructure.db.crud import UsersCrud
from auth.users.shared.infrastructure.db.users import User


# TODO: Inherit from Controller
class RetrieveAllUsersController:

    async def execute(self, request: Request) -> list[User]:
        users_crud = UsersCrud(repository=request.app.connections.mongo_client)
        retriever = AllUsersRetriever(users_crud=users_crud)
        return await retriever.execute()
