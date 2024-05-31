from models import User
from backend.repositories.base_repo import BaseRepo


class UserRepository(BaseRepo):
    model_name = User
