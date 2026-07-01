from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

class VehicleCreate(BaseModel):
    plate: str = Field(..., examples=["ABC1D23"], description="Placa do veículo (Formato antigo ou Mercosul)")
    model: str = Field(..., examples=["Volkswagen Delivery"], min_length=2)
    active: bool = True

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, v: str) -> str:
        # Normaliza a placa: remove espaços, hífens e joga para maiúsculo
        plate = v.strip().upper().replace("-", "")
        
        # Regex para validar padrão antigo (ABC1234) e Mercosul (ABC1D23)
        pattern = r"^[A-Z]{3}[0-9]{1}[A-Z0-9]{1}[0-9]{2}$"
        if not re.match(pattern, plate):
            raise ValueError("Placa inválida. Use o formato ABC1234 ou ABC1D23.")
        return plate

class VehicleResponse(BaseModel):
    id: str = Field(..., alias="_id")
    plate: str
    model: str
    active: bool
    created_at: datetime

    # Permite que o Pydantic leia dicionários do MongoDB e converta o _id implicitamente
    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: lambda v: v.isoformat()}
    }