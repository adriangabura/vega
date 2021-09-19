import abc
import typing as tp

import typing as tp
from librarius.domain.messages import AbstractMessage


class AbstractMessageUnprocessable(Exception, abc.ABC):
    def __init__(self, message: 'AbstractMessage'):
        self.message = message
