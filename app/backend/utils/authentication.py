from typing import Annotated
from datetime import timedelta, datetime

from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from app.core.config import settings



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def check_password(password: str, user_hashed_password: str):
    return not bcrypt_context.verify(password, user_hashed_password)

def hash_password(password: str):
    return bcrypt_context.hash(password)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        is_admin: bool = payload.get('is_admin')
        is_supplier: bool = payload.get('is_supplier')
        is_customer: bool = payload.get('is_customer')
        expire = payload.get('exp')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect details'
            )
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.now() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )
        return {
            'username': username,
            'id': user_id,
            'is_admin': is_admin,
            'is_supplier': is_supplier,
            'is_customer': is_customer,
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad token!'
        ) from JWTError


def create_access_token(
        username: str, 
        user_id: int, 
        is_admin: bool, 
        is_supplier: bool, 
        is_customer: bool, 
        expires_delta: timedelta 
):
    encode = {
        'sub': username, 
        'id': user_id, 
        'is_admin': is_admin, 
        'is_supplier': is_supplier, 
        'is_customer': is_customer
        }
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
