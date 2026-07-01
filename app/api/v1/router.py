from app.api.v1.endpoints import alerts, vehicles, locations 
from fastapi import APIRouter

API_ROUTER = APIRouter(prefix="/v1")
API_ROUTER.include_router(vehicles.API_ROUTER)
API_ROUTER.include_router(locations.API_ROUTER)
API_ROUTER.include_router(alerts.router)