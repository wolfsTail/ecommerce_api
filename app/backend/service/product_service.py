from slugify import slugify
from app.models import Product
from app.schemas import CreateProduct, ResponseProduct

from app.backend.utils.abstract_uow import AbstractUnitOfWork
from app.backend.utils.exceptions import (
    NoCategoryError, 
    NoProductByCategoryError,
    NoProductBySlugError,
    NoUserCredentials,
    NotTheOwnerOfProduct,
    NoItemError,
)


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
    
    async def get_product_details(
            self, product_slug: str,
    ):
        async with self.uow:
            filters = {
                "slug": product_slug,
            }
            product = await self.uow.products.get_by_filter(
                filters, self.uow.session,
            )
            if not product:
                raise NoProductBySlugError
            return product.first()
    
    async def update_product_by_slug(
            self, updated_product: CreateProduct, product_slug: str, get_user: dict,
    ):
        async with self.uow:
            filters = {
                "slug": product_slug,
            }
            product = await self.uow.products.get_by_filter(
                filters, self.uow.session,
            ).first()
            if not product:
                raise NoProductBySlugError
            
            if get_user.get('is_supplier') or get_user.get('is_admin'):
                if get_user.get('id') == product.supplier_id or get_user.get('is_admin'):
                    updated_product: dict = {
                        "name": updated_product.name,
                        "slug": slugify(updated_product.name),
                        "description": updated_product.description,
                        "price": updated_product.price,
                        "image_url": updated_product.image_url,
                        "stock": updated_product.stock,
                        "category_id": updated_product.category,
                    }
                    updated_item = await self.uow.products.update_one(
                        product.id, self.uow.session, updated_product
                    )
                    return updated_item
                raise NotTheOwnerOfProduct
            raise NoUserCredentials
    
    async def delete_product(
            self, product_id: int, get_user: dict 
    ):
        async with self.uow:
            if get_user.get('is_supplier') or get_user.get('is_admin'):
                product = await self.uow.products.get_one(product_id, self.uow.session)
                if get_user.get('id') == product.supplier_id or get_user.get('is_admin'): 
                    deleted_item_flag = await self.uow.products.delete_one(
                        product_id, self.uow.session,
                    )
                    if not deleted_item_flag:
                        raise NoItemError
                    return deleted_item_flag
                raise NotTheOwnerOfProduct
            raise NoUserCredentials
