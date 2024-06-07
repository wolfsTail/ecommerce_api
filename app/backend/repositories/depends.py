from app.backend.repositories import (
    CategoryRepository,
    ProductRepository,
    UserRepository,
    ReviewRepository,
    RatingRepository,
)

def get_category_repo() -> CategoryRepository:
    return CategoryRepository

def get_user_repo() -> UserRepository:
    return UserRepository

def get_product_repo() -> ProductRepository:
    return ProductRepository

def get_review_repo() -> ReviewRepository:
    return ReviewRepository

def get_rating_repo() -> RatingRepository:
    return RatingRepository
