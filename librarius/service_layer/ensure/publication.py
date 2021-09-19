"""
This module contains preconditions that we apply to our handlers.
"""

import typing as tp
from librarius.service_layer.ensure.abstract import AbstractMessageUnprocessable


if tp.TYPE_CHECKING:
    from librarius.service_layer.uow import AbstractUnitOfWork
    from librarius.domain.messages import AbstractMessage


class PublicationNotFound(AbstractMessageUnprocessable):
    """
    This exception is raised when we try to perform an action on a publication that doesn't exist.
    """

    def __init__(self, message: 'AbstractMessage'):
        super().__init__(message)
        self.uuid = message.uuid

def publication_exists(message: 'AbstractMessage', uow: 'AbstractUnitOfWork'):
    with uow as uow_context:
        uow_context.context.session