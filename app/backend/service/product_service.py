from slugify import slugify
from app.models import Product
from app.schemas import CreateProduct, ResponseProduct

from app.backend.utils.abstract_uow import AbstractUnitOfWork
from app.backend.utils.exceptions import NoCategoryError, NoProductByCategoryError


class ProductService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
    
    async def get_all_products(self):
        async with self.uow:
            products = await self.uow.products.get_all(self.uow.session)
        return products
    
    async def create_product(
            self, created_product: CreateProduct, get_user: dict):
        if get_user.get('is_admin') or get_user.get('is_supplier'):
            created_product: dict = {
                    "name": created_product.name,
                    "slug": slugify(created_product.name),
                    "description": created_product.description,
                    "price": created_product.price,
                    "image_url": created_product.image_url,
                    "stock": created_product.stock,
                    "category_id": created_product.category,
                    "supplier_id": get_user.get('id'),
                    "rating": 0.00,
            }
            async with self.uow:
                new_product = await self.uow.products.create_one(
                    created_product, self.uow.session
                    )
                return new_product
        return -1
    
    async def get_products_by_category(
            self, category_slug
    ):
        async with self.uow:
            filters = {
                "slug": category_slug
            }
            category = await self.uow.categories.get_by_filter(
                filters, self.uow.session
                )
            if not category:
                raise NoCategoryError
            
            filters = {
                "parent_id": category.id
            }
            subcategories = await self.uow.categories.get_by_filter(
                filters, self.uow.session
                )
            categories_and_subcategories = (
                [category.id] + [i.id for i in subcategories.all()]
            )
            products = await self.uow.products.get_products_by_categories(
                self.uow.session, categories_and_subcategories
            )
            if not products:
                raise NoProductByCategoryError
            return products

    

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
