"""
This module contains preconditions that we apply to our handlers.
"""

import typing as tp
from librarius.service_layer.ensure.abstract import AbstractMessageUnprocessable

if tp.TYPE_CHECKING:
    from librarius.service_layer.uow import AbstractUnitOfWork


