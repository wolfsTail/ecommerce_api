from models import Product
from backend.repositories.base_repo import BaseRepo


class ProductRepository(BaseRepo):
    model_name = Product
