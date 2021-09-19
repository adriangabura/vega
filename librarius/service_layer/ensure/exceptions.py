import abc
import typing as tp

from librarius.domain.messages import AbstractMessage


class AbstractMessageUnprocessable(Exception, abc.ABC):
    def __init__(self, message: 'AbstractMessage'):
        self.message = message


class PublicationNotFound(AbstractMessageUnprocessable):
    """
    This exception is raised when we try to perform an action on a publication that doesn't exist.
    """

    def __init__(self, message: 'AbstractMessage'):
        super().__init__(message)
        self.uuid = message.uuid


class PublicationAlreadyExists(AbstractMessageUnprocessable):
    """
    This exception is raised when we try to perform an action on a publication that already exists.
    """

    def __init__(self, message: 'AbstractMessage'):
        super().__init__(message)
        self.uuid = message.uuid


class AuthorNotFound(AbstractMessageUnprocessable):
    """
    This exception is raised when we try to perform an action on an author that doesn't exist.
    """

    def __init__(self, message: 'AbstractMessage'):
        super().__init__(message)
        self.uuid = message.uuid
