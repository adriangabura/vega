"""
This module contains preconditions that we apply to our handlers.
"""

import typing as tp
from librarius.service_layer.ensure import exceptions
from librarius.domain.models import Publication

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.service_layer.uow import AbstractUnitOfWork
    from librarius.domain.messages import AbstractMessage


def publication_exists(message: 'AbstractMessage', uow_context: 'AbstractUnitOfWork') -> None:
    session: 'Session' = uow_context.context.session
    publication: 'Publication' = session.query(Publication).filter_by(uuid=message.uuid)

    if publication is None:
        raise exceptions.PublicationNotFound(message)


def publication_not_exists(message: 'AbstractMessage', uow_context: 'AbstractUnitOfWork') -> None:
    session: 'Session' = uow_context.context.session
    publication: 'Publication' = session.query(Publication).filter_by(uuid=message.uuid).first()

    if publication:
        raise exceptions.PublicationAlreadyExists(message)
