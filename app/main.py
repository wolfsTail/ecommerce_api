from fastapi import FastAPI
from app.routers import routers


app = FastAPI(title="E-commerce")

for router in routers:
    app.include_router(router=router)

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to my e-commerce app"}
