import json
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.location import LocationPost, LocationEventMessage
from app.repositories.vehicle_repository import VehicleRepository


class LocationService:
    def __init__(self, db: AsyncIOMotorDatabase, publisher):
        self.db = db
        self.vehicle_repo = VehicleRepository(db)
        self.publisher = publisher  # Esse é o EventPublisher injetado do app.state

    async def receive_gps_ping(self, location_in: LocationPost) -> None:
        """Valida a existência do veículo e publica as coordenadas na fila."""
        
        # 1. Regra de Negócio: Garante que o veículo existe antes de aceitar coordenadas
        vehicle = await self.vehicle_repo.get_by_id(location_in.vehicle_id)
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veículo não encontrado. Registro de localização rejeitado."
            )
            
        if not vehicle.get("active", True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este veículo está inativo no sistema."
            )

        # 2. Prepara o payload do evento de forma padronizada
        event_payload = LocationEventMessage(
            vehicle_id=location_in.vehicle_id,
            latitude=location_in.latitude,
            longitude=location_in.longitude,
            speed=location_in.speed
        )

        # 3. Publica na Exchange do RabbitMQ de forma assíncrona
        routing_key = "gps.location.received"
        
        # .model_dump() gera um dicionário comum (dict), que é o que o seu publisher espera!
        await self.publisher.publish(
            routing_key=routing_key,
            payload=event_payload.model_dump()
        )