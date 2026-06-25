import json
from typing import Any

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractExchange


class EventPublisher:
    def __init__(self, exchange: AbstractExchange) -> None:
        self._exchange = exchange

    async def publish(self, routing_key: str, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode()
        message = Message(body=body, delivery_mode=DeliveryMode.PERSISTENT)
        await self._exchange.publish(message, routing_key=routing_key)
