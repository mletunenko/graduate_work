import asyncio

import uvicorn
from fastapi import APIRouter, FastAPI

from api.internal import router as internal_router
from api.profile import router as profile_router
from core.config import settings
from db.rabbit import RabbitMQConnection

app = FastAPI()

combined_router = APIRouter(prefix="/profiles/api")
combined_router.include_router(profile_router)
combined_router.include_router(internal_router)

app.include_router(combined_router)

if __name__ == "__main__":
    rabbit = RabbitMQConnection()
    asyncio.run(rabbit.declare_queues())

    uvicorn.run("web_server:app", host=settings.run.host, port=settings.run.port, reload=True)
