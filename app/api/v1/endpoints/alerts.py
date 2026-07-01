from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.dependencies import get_mongodb
from app.schemas.alert import AlertResponse
from app.services.alertService import AlertService

router = APIRouter(prefix="/alerts", tags=["Alertas de Monitoramento"])

@router.get("", response_model=list[AlertResponse])
async def get_active_alerts(db: AsyncIOMotorDatabase = Depends(get_mongodb)):
    """Retorna a lista de todos os alertas de velocidade ativos no sistema."""
    service = AlertService(db)
    return await service.get_unresolved_alerts()

@router.patch("/{alert_id}/resolve", status_code=status.HTTP_200_OK)
async def resolve_alert(alert_id: str, db: AsyncIOMotorDatabase = Depends(get_mongodb)):
    """Marca um alerta específico como resolvido/visto pelo operador."""
    service = AlertService(db)
    return await service.resolve_alert(alert_id)