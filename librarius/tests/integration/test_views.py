import typing as tp
from unittest import mock
from uuid import uuid4
import pytest
import logging

from sqlalchemy.orm import clear_mappers

from librarius import bootstrap
from librarius.service_layer.uow import SQLAlchemyUnitOfWork
from librarius.domain.messages import commands, queries
from librarius.domain.exceptions import SkipMessage
from librarius.domain import models

if tp.TYPE_CHECKING:
    from librarius.service_layer.message_bus import MessageBus
    from librarius.adapters.repositories.contexts import SQLAlchemyContextMaker

logger = logging.getLogger(__name__)

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


def test_create_publication_and_add_author(sqlite_bus: "MessageBus"):
    publication_uuid = str(uuid4())

    sqlite_bus.handle(commands.AddPublication(publication_uuid=publication_uuid, title="Test Publication Title"))

    author_uuid = str(uuid4())

    sqlite_bus.handle(commands.AddAuthorToPublication(
        publication_uuid=publication_uuid, author_uuid=author_uuid, author_name="Test Author Name"))

    publication: 'models.Publication' = sqlite_bus.handle(queries.PublicationByUuid(publication_uuid=publication_uuid))

    publication_authors_uuid = [author.uuid for author in publication.authors]

    assert author_uuid in publication_authors_uuid


# def test_create_author(sqlite_bus: "MessageBus"):
#     author_uuid = str(uuid4())
#
#     sqlite_bus.handle(commands.CreateAuthor(author_uuid=author_uuid, name="Author Name"))
#     result: "models.Author" = sqlite_bus.handle(queries.AuthorByUuid(author_uuid))
#     assert result.uuid == author_uuid
#
#
# def test_create_series(sqlite_bus: "MessageBus"):
#     series_uuid = str(uuid4())
#
#     sqlite_bus.handle(commands.CreateSeries(series_uuid=series_uuid, name="Series Name"))
#     result: 'models.Series' = sqlite_bus.handle(queries.SeriesByUuid(series_uuid))
#     assert result.uuid == series_uuid

