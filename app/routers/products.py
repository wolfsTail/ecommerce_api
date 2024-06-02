from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.service import ProductService
from app.backend.utils.depends import get_product_service
from app.backend.db_depends import get_db
from app.models import Product, Category
from app.schemas import CreateProduct
from app.routers.permissions import get_current_user
from app.backend.utils.exceptions import NoCategoryError, NoProductByCategoryError


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
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    query = select(Product).where(Product.slug == product_slug)
    product = await db.scalar(query)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
    return product    

@router.put("/detail/{product_slug}")
async def update_product(
    db: Annotated[AsyncSession, Depends(get_db)], 
    create_product: CreateProduct,
    product_slug: str,
    get_user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:

    query = select(Product).where(Product.slug == product_slug)
    product = await db.scalar(query)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product.supplier_id or get_user.get('is_admin'):


            active_query = update(Product).where(Product.slug == product_slug).values(
                name=create_product.name,
                slug=slugify(create_product.name),
                description=create_product.description,
                price=create_product.price,
                image_url=create_product.image_url,
                stock=create_product.stock,
                category_id=create_product.category,
            )
            await db.execute(active_query)
            await db.commit()

            return {
                "status_code": status.HTTP_200_OK,
                "transaction": 'Product update is successful',
            }
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )

@router.delete("/delete")
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], 
                         product_id: int,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    query = select(Product).where(Product.id == product_id)
    product = await db.scalar(query)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product.supplier_id or get_user.get('is_admin'):  
            active_query = update(Product).where(Product.id == product_id).values(is_active=False)
            await db.execute(active_query)
            await db.commit()
            return {
                "status_code": status.HTTP_200_OK,
                "transaction": 'Product delete is successful',
            }
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )
