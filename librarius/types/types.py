import typing as tp

from librarius.domain.messages import AbstractCommand, AbstractEvent, AbstractQuery
from librarius.service_layer.uow import AbstractUnitOfWork

if tp.TYPE_CHECKING:
    pass

Reference = tp.NewType('Reference', str)

Message = tp.TypeVar('Message', AbstractCommand, AbstractEvent, AbstractQuery) #tp.Union["AbstractCommand", "AbstractEvent", "AbstractQuery"]

EventHandler = tp.Callable[["AbstractEvent", "AbstractUnitOfWork"], tp.NoReturn]
CommandHandler = tp.Callable[["AbstractCommand", "AbstractUnitOfWork"], tp.NoReturn]
QueryHandler = tp.Callable[["AbstractQuery", "AbstractUnitOfWork"], tp.Any]

Handler = tp.Union["EventHandler", "CommandHandler", "QueryHandler"]
