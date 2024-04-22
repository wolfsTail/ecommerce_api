from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import CreateUser
from app.backend.db_depends import get_db


router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
security = HTTPBasic()


async def get_current_username(
        db: Annotated[AsyncSession, Depends(get_db)],
        credentials: HTTPBasicCredentials = Depends(security)
):
    query = select(User).where(User.username == credentials.username)
    user = await db.scalar(query)
    
    if not user or not bcrypt_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user

@router.get('/users/me')
def read_current_user(user: str = Depends(get_current_username)):
    return {'me': user}

@router.post('/')
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)], user: CreateUser
    ):
    query = insert(User).values(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password)
    )
    await db.execute(query)
    await db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }