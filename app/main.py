from fastapi import FastAPI
from loguru import logger

from app.routers import routers
from app.backend.utils.middleware import LogginMiddleware


app = FastAPI(title="E-commerce")
logger.remove()
logger.add(
    "info.log",
    rotation="1 MB",
    format="Log: [{extra[log_id]}:{level} - {time} - {message}",
    level="INFO",
    enqueue=True
)
app.add_middleware(LogginMiddleware, logging_instance=logger)

for router in routers:
    app.include_router(router=router)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to my e-commerce app"}
