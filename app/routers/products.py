from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.backend.service import ProductService
from app.backend.utils.depends import get_product_service
from app.schemas import CreateProduct
from app.routers.permissions import get_current_user
from app.backend.utils.exceptions import (
    NoCategoryError, 
    NoProductByCategoryError, 
    NoProductBySlugError,
    NoUserCredentials,
    NotTheOwnerOfProduct,
    NoItemError,
)


router = APIRouter(
    prefix="/products", 
    tags=["products"]
)


@router.get("/")
async def all_products(
    service: Annotated[ProductService, Depends(get_product_service)]
):
    products = await service.get_all_products()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products not found!"
        )
    return products
        

@router.post("/create")
async def create_product(
    service: Annotated[ProductService, Depends(get_product_service)], 
    create_product: CreateProduct,
    get_user: Annotated[dict, Depends(get_current_user)],
    ) -> dict:
        new_product = await service.create_product(
            create_product, get_user
        )
        if isinstance(new_product, int) and new_product==-1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are not authorized to use this method!'
            )
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": 'Successful',
            "created": new_product,
        }


@router.get("/{category_slug}")
async def product_by_category(
    service: Annotated[ProductService, Depends(get_product_service)],
    category_slug: str
):
    try:
        products = await service.get_products_by_category(category_slug)
        return products
    except NoCategoryError as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )
    except NoProductByCategoryError as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )

    

@router.get("/detail/{product_slug}")
async def product_detail(
    service: Annotated[ProductService, Depends(get_product_service)],
    product_slug: str
    ):
    try:
        product = await service.get_product_details(product_slug)
        return product
    except NoProductBySlugError as err:
        raise HTTPException(
            status_code=err.descr, 
            detail=err.detail
            )
    

@router.put("/{product_slug}")
async def update_product(
    service: Annotated[ProductService, Depends(get_product_service)], 
    updated_product: CreateProduct,
    product_slug: str,
    get_user: Annotated[dict, Depends(get_current_user)]
    ):
    try:
        item = await service.update_product_by_slug(
            updated_product, product_slug, get_user
        )
        return item
    except (
        NoProductBySlugError, 
        NotTheOwnerOfProduct, 
        NoUserCredentials
        ) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )


@router.delete("/delete")
async def delete_product(
    service: Annotated[ProductService, Depends(get_product_service)],
    product_id: int,
    get_user: Annotated[dict, Depends(get_current_user)]
    ):
    try:
        await service.delete_product(product_id, get_user)
        return {
            "message": "deleted!"
        }
    except ( 
        NotTheOwnerOfProduct, 
        NoUserCredentials,
        NoItemError,
        ) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )
