from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models import Product, Category
from app.schemas import CreateProduct


router = APIRouter(
    prefix="/products", 
    tags=["products"]
)


@router.get("/")
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Product).where(Product.is_active == True, Product.stock > 0)
    products = await db.scalars(query)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return products.all()    

@router.post("/create")
async def create_product(
    db: Annotated[AsyncSession, Depends(get_db)], create_product: CreateProduct
    ) -> dict:
    await db.execute(
        insert(Product).values(
            name=create_product.name,
            slug=slugify(create_product.name),
            description=create_product.description,
            price=create_product.price,
            image_url=create_product.image_url,
            stock=create_product.stock,
            category_id=create_product.category,
            rating=0.00,
        )
    )
    await db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": 'Successful',
    }

@router.get("/{category_slug}")
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):
    query = select(Category).where(Category.slug == category_slug)
    category = await db.scalar(query)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!"
        )
    subcategories = await db.scalars(select(Category).where(Category.parent_id == category.id))
    categories_and_subcategories = [category.id] + [i.id for i in subcategories.all()]
    query = select(Product).where(
        Product.is_active == True, 
        Product.stock > 0, 
        Product.category_id.in_(categories_and_subcategories)
        )
    products = await db.scalars(query)
    return products.all()
    

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
    product_slug: str
    ) -> dict:

    query = select(Product).where(Product.slug == product_slug)
    product = await db.scalar(query)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
    active_query = update(Product).where(Product.slug == product_slug).values(
        name=create_product.name,
        slug=slugify(create_product.name),
        description=create_product.description,
        price=create_product.price,
        image_url=create_product.image_url,
        stock=create_product.stock,
        category_id=create_product.category,
        rating=0.00,
    )

    await db.execute(active_query)
    await db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": 'Product update is successful',
    }

@router.delete("/delete")
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], product_id: int):
    query = select(Product).where(Product.id == product_id)
    product = await db.scalar(query)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!"
        )
    
    active_query = update(Product).where(Product.id == product_id).values(is_active=False)
    await db.execute(active_query)
    await db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": 'Product delete is successful',
    }
