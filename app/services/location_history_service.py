from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.location_repository import LocationRepository

class LocationHistoryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = LocationRepository(db)

    async def get_history_for_map(self, vehicle_id: str, limit: int) -> list[dict]:
        return await self.repo.get_vehicle_history(vehicle_id, limit)