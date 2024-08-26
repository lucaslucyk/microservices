from auth.users.shared.infrastructure.db.crud import UsersCrud
from auth.users.shared.infrastructure.db.users import User


# TODO: Inherit to UseCase
class AllUsersRetriever:
    def __init__(self, users_crud: UsersCrud):
        self.users_crud = users_crud

    async def execute(self) -> list[User]:
        return [user.to_domain() async for user in self.users_crud.get_all()]
