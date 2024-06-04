from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.user import CreateUser
from app.backend.utils.depends import get_user_service
from app.backend.service import UserService
from app.backend.utils.authentication import create_access_token, get_current_user
from app.backend.utils.exceptions import (
    NoUserError,
    IncorrectCredentailsError,
)


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
async def login(
    service: Annotated[UserService, Depends(get_user_service)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):  
    try:
        user = await service.authenticate_user(form_data.username, form_data.password)
        token = await create_access_token(
            user.username, 
            user.id, 
            user.is_admin, 
            user.is_suplier, 
            user.is_customer, 
            timedelta(minutes=5)
        )  
        return {
            'access_token': token,
            'token_type': 'bearer'
        }
    except (NoUserError, IncorrectCredentailsError) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )

@router.get('/read_current_user')
async def read_current_user(user: User = Depends(get_current_user)):
    return {'User': user}


@router.post('/')
async def create_user(
    service: Annotated[UserService, Depends(get_user_service)], 
    user: CreateUser
    ):
    await service.create_user(user)
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }
