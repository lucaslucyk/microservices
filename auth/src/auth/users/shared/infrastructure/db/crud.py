from typing import AsyncGenerator, Optional
from auth.users.shared.infrastructure.db.users import User
from shared.connections.repositories.mongo.client import MongoRepository


class UsersCrud:
    def __init__(self, repository: MongoRepository):
        self.collection = "users"
        self.repository = repository

    async def get_by_email(self, email: str) -> Optional[User]:
        doc = await self.repository.find_one(self.collection, {"email": email})
        if doc is None:
            return None
        return User.model_validate(doc)

    async def get_all(self,) -> AsyncGenerator[User, None]:
        cursor = self.repository.find_all_in(self.collection)
        async for doc in cursor:
            yield User.model_validate(doc)
