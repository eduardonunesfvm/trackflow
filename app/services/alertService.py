from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.repositories.alert_repository import AlertRepository

class AlertService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = AlertRepository(db)

    async def get_unresolved_alerts(self) -> list[dict]:
        return await self.repo.list_active_alerts()

    async def resolve_alert(self, alert_id: str) -> dict:
        success = await self.repo.mark_as_resolved(alert_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alerta não encontrado ou já resolvido."
            )
        return {"status": "success", "message": f"Alerta {alert_id} resolvido com sucesso."}