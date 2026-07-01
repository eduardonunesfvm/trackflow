from pydantic import BaseModel, Field
from datetime import datetime, timezone

class LocationPost(BaseModel):
    vehicle_id: str = Field(..., examples=["65e1c8f4b3d2a1001fbc34a5"], description="ID do veículo cadastrado no MongoDB")
    latitude: float = Field(..., examples=[-20.443], ge=-90, le=90)
    longitude: float = Field(..., examples=[-54.647], ge=-180, le=180)
    speed: float = Field(..., examples=[75.5], ge=0, description="Velocidade em km/h")

class LocationEventMessage(BaseModel):
    """Schema da mensagem estruturada que trafegará na fila do RabbitMQ"""
    vehicle_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())