from fastapi import FastAPI
from app.routers import routers


app = FastAPI(title="Commerce-API")

for router in routers:
    app.include_router(router=router)

@app.get("/")
async def welcome() -> dict:
    return {"message": "It's a root. Use `domain`/docs"}
