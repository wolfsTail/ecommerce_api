from fastapi import FastAPI
from app.routers import category, products, auth, permissions, reviews



app = FastAPI(title="E-commerce")

app.include_router(router=auth.router)
app.include_router(router=permissions.router)
app.include_router(router=category.router)
app.include_router(router=products.router)
app.include_router(router=reviews.router)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to my e-commerce app"}

