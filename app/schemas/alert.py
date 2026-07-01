from pydantic import BaseModel, Field
from datetime import datetime

class AlertResponse(BaseModel):
    id: str = Field(..., alias="_id")
    vehicle_id: str
    latitude: float
    longitude: float
    speed_registered: float
    speed_limit: float
    triggered_at: datetime
    resolved: bool

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: lambda v: v.isoformat()}
    }