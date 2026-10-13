from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router
from src.exception_registry import ExceptionRegistry
from src.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="News API",
    root_path="/api/v1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
ExceptionRegistry.apply(app)
