from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDBClient:
    def __init__(self, uri: str, database_name: str) -> None:
        self._uri = uri
        self._database_name = database_name
        self._client: AsyncIOMotorClient | None = None
        self._database: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        self._client = AsyncIOMotorClient(self._uri)
        self._database = self._client[self._database_name]
        await self._client.admin.command("ping")

    async def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None

    @property
    def database(self) -> AsyncIOMotorDatabase:
        if self._database is None:
            msg = "MongoDB client is not connected"
            raise RuntimeError(msg)
        return self._database
