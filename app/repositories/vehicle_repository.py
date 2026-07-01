from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.vehicle import VehicleCreate
from datetime import datetime
from bson import ObjectId

class VehicleRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["vehicles"]

    async def get_by_plate(self, plate: str) -> dict | None:
        return await self.collection.find_one({"plate": plate})

    async def get_by_id(self, vehicle_id: str) -> dict | None:
        if not ObjectId.is_valid(vehicle_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(vehicle_id)})

    async def create(self, vehicle_in: VehicleCreate) -> dict:
        document = vehicle_in.model_dump()
        document["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return document

    async def list_all(self) -> list[dict]:
        cursor = self.collection.find()
        vehicles = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            vehicles.append(doc)
        return vehicles