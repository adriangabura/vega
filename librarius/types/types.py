import typing as tp
import typing_extensions as tp_e

if tp.TYPE_CHECKING:
    from librarius.domain.commands import AbstractCommand
    from librarius.domain.events import AbstractEvent
    from librarius.domain.queries import AbstractQuery
    from librarius.service_layer.uow import AbstractUnitOfWork

Reference = tp.NewType('Reference', str)

Message = tp.Union["AbstractCommand", "AbstractEvent", "AbstractQuery"]

EventHandler = tp.Callable[["AbstractEvent", "AbstractUnitOfWork"], tp.NoReturn]
CommandHandler = tp.Callable[["AbstractCommand", "AbstractUnitOfWork"], tp.NoReturn]
QueryHandler = tp.Callable[["AbstractQuery", "AbstractUnitOfWork"], tp.Any]

Handler = tp.Union["EventHandler", "CommandHandler", "QueryHandler"]
