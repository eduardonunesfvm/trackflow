from collections.abc import Callable

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.lifespan import lifespan


def create_app(
    *,
    lifespan_override: Callable | None = None,
) -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="TrackFlow API — Event-Driven Architecture",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan_override or lifespan,
    )

    application.include_router(health_router)
    application.include_router(api_router, prefix=settings.api_v1_prefix)

    return application


app = create_app()
