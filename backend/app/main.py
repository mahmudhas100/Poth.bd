from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.db.session import init_db_pragmas
from app.services.stop_service import init_stop_cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db_pragmas()
    init_stop_cache()
    yield
    # Shutdown logic (if needed)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Poth.bd (পথ) Transit API - Bus Fare & Route Engine",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
