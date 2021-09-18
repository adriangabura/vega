import typing as tp
from unittest import mock
from uuid import uuid4
import pytest

from sqlalchemy.orm import clear_mappers

from librarius import bootstrap
from librarius.service_layer.uow import SQLAlchemyUnitOfWork
from librarius.domain.messages import commands, queries

if tp.TYPE_CHECKING:
    from librarius.service_layer.message_bus import MessageBus
    from librarius.adapters.repository_contexts import SQLAlchemyContextMaker


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
    sqlite_bus.handle(commands.AddPublication("cerbulan", str(uuid4())))
    results = sqlite_bus.handle(queries.AllPublications())
    print("results:", results)
