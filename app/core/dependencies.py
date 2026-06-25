from aio_pika.abc import AbstractChannel
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.events.publisher import EventPublisher
from app.infrastructure.messaging.rabbitmq import RabbitMQBroker
from app.infrastructure.mongodb.client import MongoDBClient


def get_mongodb(request: Request) -> AsyncIOMotorDatabase:
    mongodb: MongoDBClient = request.app.state.mongodb
    return mongodb.database


def get_rabbitmq_channel(request: Request) -> AbstractChannel:
    rabbitmq: RabbitMQBroker = request.app.state.rabbitmq
    return rabbitmq.channel


def get_event_publisher(request: Request) -> EventPublisher:
    return request.app.state.event_publisher
