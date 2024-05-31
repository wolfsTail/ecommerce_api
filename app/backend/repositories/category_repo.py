from app.models import Category
from app.backend.repositories.base_repo import BaseRepo


class CategoryRepository(BaseRepo):
    model_name = Category
