from app.routers import category, products, auth, permissions, reviews

routers = [
    category.router,
    products.router,
    auth.router,
    permissions.router,
    reviews.router,
]