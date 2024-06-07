from app.backend.utils.abstract_uow import AbstractUnitOfWork

from app.backend.utils.authentication import check_password, hash_password
from app.schemas.user import CreateUser
from app.backend.utils.exceptions import (
    YouAreNotAdmin,
    NoItemError,
    NoUserError,
    IncorrectCredentailsError,
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
                raise NoUserError
            return current_user
        
    async def _get_current_user_by_username(self, username: str):
        async with self.uow:
            filters = {
                "username": username,
            }
            current_user = await self.uow.users.get_by_filter(
                filters, self.uow.session
            ).first()
            if not current_user or not current_user.is_active:
                raise NoUserError
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
    
    async def authenticate_user(
            self, username: str, password: str
    ):
        async with self.uow:
            user = await self._get_current_user_by_username(username)

            if check_password(password, user.hashed_password):
                raise IncorrectCredentailsError
            
            return user
    
    async def create_user(
            self, user: CreateUser
    ):
        async with self.uow:
            values = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "hashed_password": hash_password(user.password)
            }
            await self.uow.users.create_one(values, self.uow.session)
            return None    
