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


@pytest.fixture
def sqlite_bus(sql_alchemy_context_factory: "SQLAlchemyContextMaker", casbin_enforcer):
    bus = bootstrap.bootstrap(
        start_orm=False,
        uow=GenericUnitOfWork(context_factory=sql_alchemy_context_factory, casbin_enforcer=casbin_enforcer),
        notifications=mock.Mock(),
        publish=lambda *args: None
    )
    yield bus
    clear_mappers()