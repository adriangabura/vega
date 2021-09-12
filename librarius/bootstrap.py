import inspect
import typing as tp
from librarius.adapters import orm, redis_eventpublisher
from librarius.adapters.notifications import MemoryNotification
from librarius.service_layer import handlers, message_bus, uow as uow_package
from librarius.service_layer.handlers import sqlalchemy_query_handlers

if tp.TYPE_CHECKING:
    from librarius.types import Message
    from librarius.service_layer import AbstractUnitOfWork
    from librarius.adapters.notifications import AbstractNotification
    from librarius.domain.events import AbstractEvent
    from librarius.domain.commands import AbstractCommand
    from librarius.domain.queries import AbstractQuery


def inject_dependencies(handler: tp.Callable, dependencies: dict) -> tp.Callable[["Message"], tp.Union[tp.Any, None]]:
    params = inspect.signature(handler).parameters
    deps: dict[str, tp.Union[tp.Callable, tp.Type]] = {name: dependency for name, dependency in dependencies.items() if name in params}

    def handler_with_injections(message: "Message") -> tp.Union[tp.Any, None]:
        return handler(message, **deps)

    return handler_with_injections


def bootstrap(
        start_orm: bool = True,
        uow: "AbstractUnitOfWork" = uow_package.SQLAlchemyUnitOfWork(),
        notifications: "AbstractNotification" = None,
        publish: tp.Callable = redis_eventpublisher.publish
) -> message_bus.MessageBus:

    if notifications is None:
        notifications = MemoryNotification()

    if start_orm:
        orm.start_mappers()

    dependencies: dict = {
        "uow": uow,
        "notifications": notifications,
        "publish": publish
    }
    injected_event_handlers: dict[tp.Type["AbstractEvent"], list[tp.Callable]] = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers: dict[tp.Type["AbstractCommand"], tp.Callable] = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    injected_query_handlers: dict[tp.Type["AbstractQuery"], tp.Callable] = {
        query_type: inject_dependencies(handler, dependencies)
        for query_type, handler in sqlalchemy_query_handlers.QUERY_HANDLERS.items()
    }

    return message_bus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
        query_handlers=injected_query_handlers
    )
