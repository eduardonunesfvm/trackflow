from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange

EVENTS_EXCHANGE = "trackflow.events"


class RabbitMQBroker:
    def __init__(self, uri: str) -> None:
        self._uri = uri
        self._connection: AbstractConnection | None = None
        self._channel: AbstractChannel | None = None
        self._exchange: AbstractExchange | None = None

    async def connect(self) -> None:
        self._connection = await connect_robust(self._uri)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            EVENTS_EXCHANGE,
            ExchangeType.TOPIC,
            durable=True,
        )

    async def disconnect(self) -> None:
        if self._connection is not None and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None
        self._exchange = None

    @property
    def channel(self) -> AbstractChannel:
        if self._channel is None:
            msg = "RabbitMQ broker is not connected"
            raise RuntimeError(msg)
        return self._channel

    @property
    def exchange(self) -> AbstractExchange:
        if self._exchange is None:
            msg = "RabbitMQ exchange is not initialized"
            raise RuntimeError(msg)
        return self._exchange
