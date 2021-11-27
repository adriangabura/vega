import typing as tp

from librarius.domain.messages import AbstractCommand, AbstractEvent, AbstractQuery
from librarius.service.uow import AbstractUnitOfWork

if tp.TYPE_CHECKING:
    pass

Reference = tp.NewType("Reference", str)
