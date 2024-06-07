from app.models import User
from app.backend.repositories.base_repo import BaseRepo


class UserRepository(BaseRepo):
    model_name = User
