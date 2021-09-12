import typing as tp

#if tp.TYPE_CHECKING:
#    from librarius.domain.commands import AbstractCommand
#    from librarius.domain.events import AbstractEvent
#    from librarius.domain.queries import AbstractQuery



Reference = str
#References = typing.Union[list[Reference], tuple[Reference, ...]]

#Entities = typing.Union[list[Entity], tuple[Entity, ...]]

Message = tp.Union["AbstractCommand", "AbstractEvent", "AbstractQuery"]

EventHandler: tp.Type = tp.Callable[["AbstractEvent", "AbstractUnitOfWork"], None]
CommandHandler: tp.Type = tp.Callable[["AbstractCommand", "AbstractUnitOfWork"], None]
QueryHandler: tp.Type = tp.Callable[["AbstractQuery", "AbstractUnitOfWork"], tp.Any]
