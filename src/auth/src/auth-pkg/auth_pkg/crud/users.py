from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.base import CRUDBase
from ..models.users import User as UserModel
from ..schemas.admin import UserCreateDB, UserUpdate, UserActivate


class CRUDUser(CRUDBase[UserModel, UserCreateDB, UserUpdate]):

    async def activate(
        self,
        db: AsyncSession,
        *,
        data: UserActivate
    ) -> UserModel:
        user = await self.find_one(db=db, uuid=data.uid, token=data.token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )
        
        # update and save
        user.is_active = True
        return await self.save(db=db, obj=user)


users = CRUDUser(UserModel)