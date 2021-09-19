import typing as tp
from unittest import mock
from uuid import uuid4
import pytest
import logging

from sqlalchemy.orm import clear_mappers

from librarius import bootstrap
from librarius.service_layer.uow import SQLAlchemyUnitOfWork
from librarius.domain.messages import commands, queries

if tp.TYPE_CHECKING:
    from librarius.service_layer.message_bus import MessageBus
    from librarius.adapters.repositories.contexts import SQLAlchemyContextMaker


@pytest.fixture
def sqlite_bus(sql_alchemy_context_factory: "SQLAlchemyContextMaker"):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=SQLAlchemyUnitOfWork(
            context_factory=sql_alchemy_context_factory,
        ),
        notifications=mock.Mock(),
        publish=lambda *args: None
    )
    yield bus
    clear_mappers()


def test_handle_view(sqlite_bus: "MessageBus"):
    publication_uuid = str(uuid4())

    sqlite_bus.handle(commands.AddPublication("cerbulan", publication_uuid))
    results = sqlite_bus.handle(queries.AllPublications())
    logger = logging.getLogger(__name__)
    logger.info(f'results: {results}')
