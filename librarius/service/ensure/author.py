"""
This module contains preconditions that we apply to our handlers.
"""

import typing as tp
from librarius.service.ensure import exceptions
from librarius.domain.models import Author
from librarius.domain.exceptions import SkipMessage

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.service.uow import AbstractUnitOfWork
    from librarius.domain.messages import AbstractMessage


def old_author_not_exists_skip(
    message: "AbstractMessage", uow_context: "AbstractUnitOfWork"
) -> None:
    session: "Session" = uow_context.context.session
    author: "Author" = (
        session.query(Author)
        .filter_by(uuid=message.author_uuid, name=message.name)
        .first()
    )

    if author:
        raise SkipMessage(
            f"Author with uuid {message.author_uuid} and name {message.name} exists"
        )


def old_author_exists(message: "AbstractMessage", uow_context: "AbstractUnitOfWork"):
    session: "Session" = uow_context.context.session
    author: "Author" = (
        session.query(Author)
        .filter_by(uuid=message.author_uuid, name=message.author_name)
        .first()
    )

    if not author:
        raise exceptions.AuthorNotFound(message)
