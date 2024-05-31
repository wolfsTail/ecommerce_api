from models import Category
from backend.repositories.base_repo import BaseRepo


class CategoryRepository(BaseRepo):
    model_name = Category
