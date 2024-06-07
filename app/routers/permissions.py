from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.backend.service import UserService
from app.backend.utils.depends import get_user_service
from app.routers.auth import get_current_user
from app.backend.utils.exceptions import (
    YouAreNotAdmin,
    NoItemError,
)


router = APIRouter(
    prefix='/permission', tags=['permission']
)


@router.patch('/')
async def set_supplier_permission(
    service: Annotated[UserService, Depends(get_user_service)],
    get_user: Annotated[dict, Depends(get_current_user)],
    user_id: int
):
    try:
        detail = await service.set_permissions(
            user_id, get_user
        )
        return {
                'status_code': status.HTTP_200_OK,
                'detail': detail,
            }
    except (
        YouAreNotAdmin,
        NoItemError,
    ) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )


@router.delete('/delete')
async def delete_user(
    service: Annotated[UserService, Depends(get_user_service)],
    get_user: Annotated[dict, Depends(get_current_user)],
    user_id: int,
):
        try:
            detail = await service.set_user_status(user_id, get_user)
            return {
                'status_code': status.HTTP_200_OK,
                'detail': detail
            }
        except (
            YouAreNotAdmin,
            NoItemError,
        ) as err:
            raise HTTPException(
                status_code=err.descr, detail=err.detail
            )       
