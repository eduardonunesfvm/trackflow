from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

class AlertRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["alerts"]

    async def list_active_alerts(self) -> list[dict]:
        """Retorna apenas os alertas que ainda não foram resolvidos/limpos."""
        cursor = self.collection.find({"resolved": False}).sort("triggered_at", -1)
        alerts = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            alerts.append(doc)
        return alerts

    async def mark_as_resolved(self, alert_id: str) -> bool:
        """Permite que o operador marque um alerta de velocidade como resolvido."""
        if not ObjectId.is_valid(alert_id):
            return False
        result = await self.collection.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {"resolved": True, "resolved_at": datetime.utcnow()}}
        )
        return result.modified_count > 0