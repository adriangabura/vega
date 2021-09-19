"""
This module contains preconditions that we apply to our handlers.
"""

import typing as tp
from librarius.service_layer.ensure import exceptions
from librarius.domain.models import Series
from librarius.domain.exceptions import SkipMessage

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.service_layer.uow import AbstractUnitOfWork
    from librarius.domain.messages import AbstractMessage


def series_not_exists_skip(message: 'AbstractMessage', uow_context: 'AbstractUnitOfWork') -> None:
    session: 'Session' = uow_context.context.session
    series: 'Series' = session.query(Series).filter_by(uuid=message.series_uuid, name=message.name).first()

    if series:
        raise SkipMessage(f"Series with uuid {message.series_uuid} and name {message.name} exists")