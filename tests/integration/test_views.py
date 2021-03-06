import typing as tp
from unittest import mock
from uuid import uuid4
import pytest
import logging

from sqlalchemy.orm import clear_mappers

from librarius import bootstrap
from librarius.service.uow import GenericUnitOfWork
from librarius.domain.messages import commands, queries
from librarius.domain.exceptions import SkipMessage
from librarius.domain import models

if tp.TYPE_CHECKING:
    from librarius.service.message_bus import MessageBus
    from librarius.adapters.repositories.contexts import SQLAlchemyContextMaker

logger = logging.getLogger(__name__)


pytestmark = pytest.mark.usefixtures("casbin_policy_blank")


def test_resources_and_roles(sqlite_bus):
    resource_uuid = str(uuid4())
    role_uuid = str(uuid4())
    sqlite_bus.handle(
        commands.CreateResource(name="/users/", resource_uuid=resource_uuid)
    )
    sqlite_bus.handle(
        commands.CreateRole(name="driver", role_uuid=role_uuid, resource_names=["/users/"])
    )

# @pytest.fixture
# def generate_uuids():
#     class IdGen:
#         def __init__(self):
#             self.publication1 = str(uuid4())
#             self.publication2 = str(uuid4())
#             self.author1 = str(uuid4())
#             self.author2 = str(uuid4())
#             self.series1 = str(uuid4())
#             self.series2 = str(uuid4())
#
#     return IdGen()


# def test_create_publication(sqlite_bus: "MessageBus", generate_uuids):
#     publication_uuid = generate_uuids.publication1
#     sqlite_bus.handle(
#         commands.CreatePublication(
#             publication_uuid=publication_uuid, title="Test Publication Title"
#         )
#     )
#     result: "models.Publication" = sqlite_bus.handle(
#         queries.PublicationByUuid(publication_uuid)
#     )
#
#     assert publication_uuid == result.uuid


# def test_add_nonexistent_author_to_publication(
#     sqlite_bus: "MessageBus", generate_uuids
# ):
#
#     author_uuid = generate_uuids.author1
#     publication_uuid = generate_uuids.publication1
#
#     sqlite_bus.handle(
#         commands.AddAuthorToPublication(
#             publication_uuid=publication_uuid,
#             author_uuid=author_uuid,
#             author_name="Test Author Name",
#         )
#     )
#
#     publication: "models.Publication" = sqlite_bus.handle(
#         queries.PublicationByUuid(publication_uuid=publication_uuid)
#     )
#
#     publication_authors_uuid = [author.uuid for author in publication.authors]
#
#     assert author_uuid not in publication_authors_uuid


# def test_add_publication_to_series(sqlite_bus: "MessageBus", generate_uuids):
#     publication_uuid = generate_uuids.publication1
#     series_uuid = generate_uuids.series1
#
#     sqlite_bus.handle(commands.CreateSeries(series_uuid, "Some series"))
#
#     sqlite_bus.handle(
#         commands.AddPublicationToSeries(
#             series_uuid=series_uuid,
#             series_name="Test Series",
#             publication_uuid=publication_uuid,
#         )
#     )
#
#     series: "models.Series" = sqlite_bus.handle(
#         queries.SeriesByUuid(series_uuid=series_uuid)
#     )
#     if series:
#         series_publications_uuid = [
#             publication.uuid for publication in series.publications
#         ]
#         assert publication_uuid in series_publications_uuid


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
