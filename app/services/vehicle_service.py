from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.schemas.vehicle import VehicleCreate
from app.repositories.vehicle_repository import VehicleRepository

class VehicleService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = VehicleRepository(db)

    async def register_vehicle(self, vehicle_in: VehicleCreate) -> dict:
        """Aplica regras de negócio para criação de um novo veículo."""
        # Verifica se já existe um veículo com a mesma placa
        existing_vehicle = await self.repo.get_by_plate(vehicle_in.plate)
        if existing_vehicle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um veículo cadastrado com esta placa."
            )
            
        # Se passar na validação, envia para o banco persistir
        return await self.repo.create(vehicle_in)

    async def get_all_vehicles(self) -> list[dict]:
        """Recupera todos os veículos da frota."""
        return await self.repo.list_all()