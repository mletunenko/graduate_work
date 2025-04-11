import uvicorn
from fastapi import APIRouter, FastAPI

from api.profile import router as profile_router
from core.config import settings

app = FastAPI()

combined_router = APIRouter(prefix="/api")
combined_router.include_router(profile_router)

app.include_router(combined_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
