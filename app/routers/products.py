from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from slugify import slugify
from app.backend.db_depends import get_db

from app.models import Product
from app.schemas import CreateProduct


router = APIRouter(
    prefix="/products", 
    tags=["products"]
)


@router.get("/")
async def all_products(db: Annotated[Session, Depends(get_db)]):
    query = select(Product).where(Product.is_active == True, Product.stock > 0)
    products = db.scalars(query).all()
    return products    

@router.post("/create")
async def create_product(
    db: Annotated[Session, Depends(get_db)], create_product: CreateProduct
    ) -> dict:
    db.execute(
        insert(Product).values(
            name=create_product.name,
            slug=slugify(create_product.name),
            description=create_product.description,
            price=create_product.price,
            image_url=create_product.url,
            stock=create_product.stock,
            category=create_product.category,
        )
    )
    db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "OK!"
    }

@router.get("/{category_slug}")
async def product_by_category(category_slug: str):
    ...

@router.get("/detail/{product_slug}")
async def product_detail(product_slug: str):
    ...

@router.put("/detail/{product_slug}")
async def update_product(product_slug: str):
    ...

@router.delete("/delete")
async def delete_product(product_id: int):
    ...
