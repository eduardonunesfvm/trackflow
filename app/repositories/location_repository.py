from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class LocationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["locations"]

    async def get_vehicle_history(self, vehicle_id: str, limit: int = 100) -> list[dict]:
        """Busca o histórico de coordenadas ordenadas das mais recentes para as mais antigas."""
        cursor = self.collection.find({"vehicle_id": vehicle_id}).sort("timestamp", -1).limit(limit)
        history = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            history.append(doc)
        return history