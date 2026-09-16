from fastapi import APIRouter
from app.api.endpoints import health, stops, fare

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(stops.router, tags=["Stops"])
api_router.include_router(fare.router, tags=["Fare Search"])
