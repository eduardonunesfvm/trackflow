import json
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

class LocationConsumerService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.location_collection = db["locations"]
        self.alert_collection = db["alerts"]

    async def process_location_event(self, payload_dict: dict) -> None:
        """Processa a coordenada do GPS, salva no banco e gera alertas se necessário."""
        try:
            # 1. Adiciona o timestamp de processamento do servidor
            payload_dict["processed_at"] = datetime.utcnow()
            
            # 2. Salva o histórico de localização no MongoDB
            await self.location_collection.insert_one(payload_dict)
            logger.info(f"📍 Localização registrada para o veículo {payload_dict['vehicle_id']}")

            # 3. Regra de Negócio: Verifica excesso de velocidade
            speed = payload_dict.get("speed", 0.0)
            if speed > settings.speed_limit:
                alert_document = {
                    "vehicle_id": payload_dict["vehicle_id"],
                    "latitude": payload_dict["latitude"],
                    "longitude": payload_dict["longitude"],
                    "speed_registered": speed,
                    "speed_limit": settings.speed_limit,
                    "triggered_at": datetime.utcnow(),
                    "resolved": False
                }
                # Salva o alerta gerado em outra collection do NoSQL
                await self.alert_collection.insert_one(alert_document)
                logger.warning(f"🚨 ALERTA DE VELOCIDADE: Veículo {payload_dict['vehicle_id']} a {speed}km/h (Limite: {settings.speed_limit}km/h)!")

        except Exception as e:
            logger.error(f"Erro ao processar evento de localização: {e}")
            raise e