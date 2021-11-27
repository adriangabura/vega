"""
This module contains preconditions that we apply to our handlers.
"""

import typing as tp
from librarius.service.ensure import exceptions
from librarius.domain.models import Publication

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.service.uow import AbstractUnitOfWork
    from librarius.domain.messages import AbstractMessage


def publication_exists(
    message: "AbstractMessage", uow_context: "AbstractUnitOfWork"
) -> None:
    session: "Session" = uow_context.context.session
    publication: "Publication" = session.query(Publication).filter_by(
        uuid=message.publication_uuid
    )

    if publication is None:
        raise exceptions.PublicationNotFound(message)


def publication_not_exists(
    message: "AbstractMessage", uow_context: "AbstractUnitOfWork"
) -> None:
    session: "Session" = uow_context.context.session
    publication: "Publication" = (
        session.query(Publication).filter_by(uuid=message.publication_uuid).first()
    )

    if publication:
        raise exceptions.PublicationAlreadyExists(message)


def publication_skip_exists(
    message: "AbstractMessage", uow_context: "AbstractUnitOfWork"
) -> None:
    session: "Session" = uow_context.context.session
    publication: "Publication" = (
        session.query(Publication).filter_by(uuid=message.publication_uuid).first()
    )
    from librarius.domain.exceptions import SkipMessage

    if publication:
        raise SkipMessage(f"Publication with uuid {message.publication_uuid} exists")
