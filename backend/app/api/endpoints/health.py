from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def root():
    return {"status": "ok", "app": settings.PROJECT_NAME, "version": settings.VERSION}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}
