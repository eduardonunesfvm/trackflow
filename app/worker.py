import asyncio
import logging
import sys
from aio_pika import connect_robust, IncomingMessage
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.services.location_consumer_service import LocationConsumerService
import json

# Configuração básica de logs no terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("trackflow.worker")

async def on_message(message: IncomingMessage, consumer_service: LocationConsumerService):
    """Callback executado toda vez que uma nova mensagem chega na fila."""
    async with message.process(): # Garante o 'ack' automático se o bloco terminar com sucesso
        try:
            logger.info(f"📩 Mensagem recebida da fila: {message.routing_key}")
            
            # Decodifica o corpo binário da mensagem em dicionário Python
            payload = json.loads(message.body.decode())
            
            # Envia para a camada de serviço processar e salvar no Mongo
            await consumer_service.process_location_event(payload)
            
        except Exception as e:
            logger.error(f"Falha crítica no processamento da mensagem: {e}")
            # Em caso de erro, a mensagem volta para a fila ou vai para DLQ dependendo da estratégia

async def main():
    logger.info("Iniciando o Worker do TrackFlow...")

    # 1. Inicializa conexão assíncrona com o MongoDB
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    db = mongo_client[settings.mongo_db]
    consumer_service = LocationConsumerService(db)
    logger.info("🔌 Conectado ao MongoDB com sucesso.")

    # 2. Inicializa conexão robusta com o RabbitMQ (reconecta sozinho se cair)
    connection = await connect_robust(settings.rabbitmq_uri)
    channel = await connection.channel()
    
    # 3. Garante que a Exchange declarada na API existe aqui também
    exchange = await channel.declare_exchange(
        name="trackflow.events", 
        type="topic", 
        durable=True
    )

    # 4. Cria e declara a Fila de forma automática
    queue_name = "gps.location.received"
    queue = await channel.declare_queue(name=queue_name, durable=True)

    # 5. Faz o Binding (vínculo entre a exchange e a fila através da routing_key)
    routing_key = "gps.location.received"
    await queue.bind(exchange=exchange, routing_key=routing_key)
    logger.info(f"🔗 Fila '{queue_name}' vinculada à exchange com a chave '{routing_key}'.")

    logger.info("🚀 Worker aguardando novas mensagens na fila. Para sair use CTRL+C")

    # 6. Começa a escutar a fila atrelando a função de callback
    await queue.consume(lambda msg: on_message(msg, consumer_service))

    # Mantém o loop rodando infinitamente
    try:
        await asyncio.Future()
    finally:
        await connection.close()
        mongo_client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker encerrado pelo usuário.")
        sys.exit(0)