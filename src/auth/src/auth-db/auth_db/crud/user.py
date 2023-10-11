from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from ..models.users import User as UserModel
from ..schemas.admin import UserCreateDB, UserUpdate, UserActivate
from ..exceptions.db import UserActivateException


class CRUDUser(CRUDBase[UserModel, UserCreateDB, UserUpdate]):
    async def activate(
        self, db: AsyncSession, *, data: UserActivate
    ) -> UserModel:
        user = await self.find_one(db=db, uid=data.uid, token=data.token)
        if not user:
            raise UserActivateException(
                f"{self.model.__name__} or token not found"
            )

        if user.is_active:
            raise UserActivateException(
                f"{self.model.__name__} is already active"
            )
        
        # update and save
        user.is_active = True
        return await self.save(db=db, obj=user)


users = CRUDUser(UserModel)
