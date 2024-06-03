from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.utils.abstract_uow import AbstractUnitOfWork
from app.routers.auth import get_current_user
from app.models.user import User
from app.backend.db_depends import get_db
from app.backend.utils.exceptions import (
    YouAreNotAdmin,
    NoItemError,
)


class UserService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
    
    @staticmethod
    def _is_admin(get_user: dict):
        if not get_user.get("is_admin"):
            raise YouAreNotAdmin        

    async def _get_current_user(self, user_id: int):
        async with self.uow:
            current_user = await self.uow.users.get_one(
                user_id, self.uow.session
            )
            if not current_user:
                raise NoItemError
            return current_user
    
    async def set_permissions(
            self, user_id: int, get_user: dict
    ):
        self._is_admin(get_user)
        user = await self._get_current_user(user_id)

        async with self.uow:
            if user.is_suplier:
                values = {
                    "is_suplier": False, "is_customer": True
                }
                await self.uow.users.update_one(user_id, self.uow.session, values)
                return 'User is no longer supplier'
            else:
                values = {
                    "is_suplier": True, "is_customer": False
                }
                await self.uow.users.update_one(user_id, self.uow.session, values)
                return 'User is now supplier'
    
    async def set_user_status(
            self, user_id: int, get_user: dict
    ):
        self._is_admin(get_user)
        user = await self._get_current_user(user_id)

        async with self.uow:
            if user.is_active:
                values = {
                    "is_active": False,
                }
                await self.uow.users.update_one(user_id, self.uow.session, values)
                return "User is deactivated!"
            else:
                values = {
                    "is_active": True,
                }
                await self.uow.users.update_one(user_id, self.uow.session, values)
                return "User is activated!"                
