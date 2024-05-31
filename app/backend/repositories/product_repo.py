from app.models import Product
from app.backend.repositories.base_repo import BaseRepo


class ProductRepository(BaseRepo):
    model_name = Product
