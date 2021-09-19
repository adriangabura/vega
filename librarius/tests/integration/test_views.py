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

from librarius.service_layer.ensure import exceptions
def test_handle_view(sqlite_bus: "MessageBus"):
    logger = logging.getLogger(__name__)
    publication_uuid = str(uuid4())
    publication_uuid2 = str(uuid4())
    logger.info(publication_uuid)

    try:
        sqlite_bus.handle(commands.AddPublication(title="cerbulan", uuid=publication_uuid))
        sqlite_bus.handle(commands.AddPublication(title="cerbulan", uuid=publication_uuid))
        results = sqlite_bus.handle(queries.AllPublications())

        logger.info(f'results: {results}')
    except exceptions.PublicationAlreadyExists as error:
        logger.error(error)
