from fastapi import APIRouter, Depends, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.dependencies import get_mongodb  # Ajuste o import se necessário
from app.models.location import LocationPost
from app.services.locationService import LocationService

API_ROUTER = APIRouter(prefix="/locations", tags=["Localizações"])

@API_ROUTER.post("", status_code=status.HTTP_202_ACCEPTED)
async def receive_location(
    location_in: LocationPost, 
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_mongodb)
):
    """
    Recebe as coordenadas de telemetria do dispositivo GPS de forma assíncrona.
    Retorna 202 Accepted imediatamente após publicar na fila de mensageria.
    """
    # Recupera o publisher instanciado no startup da aplicação
    publisher = request.app.state.event_publisher
    
    service = LocationService(db, publisher)
    await service.receive_gps_ping(location_in)
    
    return {"status": "Event published successfully", "queue": "gps.location.received"}