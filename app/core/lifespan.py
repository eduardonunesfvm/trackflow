from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.events.publisher import EventPublisher
from app.infrastructure.messaging.rabbitmq import RabbitMQBroker
from app.infrastructure.mongodb.client import MongoDBClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    mongodb = MongoDBClient(settings.mongo_uri, settings.mongo_db)
    rabbitmq = RabbitMQBroker(settings.rabbitmq_uri)

    await mongodb.connect()
    await rabbitmq.connect()

    app.state.mongodb = mongodb
    app.state.rabbitmq = rabbitmq
    app.state.event_publisher = EventPublisher(rabbitmq.exchange)

    yield

    await rabbitmq.disconnect()
    await mongodb.disconnect()


def create_lifespan(
    *,
    mongodb_factory: type[MongoDBClient] = MongoDBClient,
    rabbitmq_factory: type[RabbitMQBroker] = RabbitMQBroker,
) -> Callable:
    @asynccontextmanager
    async def custom_lifespan(app: FastAPI) -> AsyncIterator[None]:
        mongodb = mongodb_factory(settings.mongo_uri, settings.mongo_db)
        rabbitmq = rabbitmq_factory(settings.rabbitmq_uri)

        await mongodb.connect()
        await rabbitmq.connect()

        app.state.mongodb = mongodb
        app.state.rabbitmq = rabbitmq
        app.state.event_publisher = EventPublisher(rabbitmq.exchange)

        yield

        await rabbitmq.disconnect()
        await mongodb.disconnect()

    return custom_lifespan
