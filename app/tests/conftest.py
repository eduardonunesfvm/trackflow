from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app


@asynccontextmanager
async def test_lifespan(app: FastAPI) -> AsyncIterator[None]:
    mongodb = MagicMock()
    mongodb.database = MagicMock()

    rabbitmq = MagicMock()
    rabbitmq.channel = AsyncMock()
    rabbitmq.exchange = AsyncMock()

    event_publisher = MagicMock()
    event_publisher.publish = AsyncMock()

    app.state.mongodb = mongodb
    app.state.rabbitmq = rabbitmq
    app.state.event_publisher = event_publisher

    yield


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app(lifespan_override=test_lifespan)
    with TestClient(app) as test_client:
        yield test_client
