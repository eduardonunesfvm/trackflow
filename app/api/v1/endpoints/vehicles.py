from fastapi import APIRouter
from app.models.vehicle import VehicleCreate, VehicleResponse
from app.services.vehicle_service import VehicleService
from fastapi import Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.dependencies import get_mongodb

API_ROUTER = APIRouter(prefix="/vehicles", tags=["Veículos"])

@API_ROUTER.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle_in: VehicleCreate, db: AsyncIOMotorDatabase = Depends(get_mongodb)):
    # Inicializa o serviço injetando o banco
    service = VehicleService(db)
    # Delega toda a execução para a camada de serviço
    return await service.register_vehicle(vehicle_in)

@API_ROUTER.get("", response_model=list[VehicleResponse])
async def list_vehicles(db: AsyncIOMotorDatabase = Depends(get_mongodb)):
    service = VehicleService(db)
    return await service.get_all_vehicles()