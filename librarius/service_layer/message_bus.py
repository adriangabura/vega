import logging
import typing as tp
from librarius.domain import commands, events, queries
from librarius.types import Message
from librarius.service_layer.uow import AbstractUnitOfWork

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(
            self,
            uow: AbstractUnitOfWork,
            event_handlers: dict[tp.Type[events.AbstractEvent], list[tp.Callable]],
            command_handlers: dict[tp.Type[commands.AbstractCommand], tp.Callable],
            query_handlers: dict[tp.Type[queries.AbstractQuery], tp.Callable]
    ):
        self.queue: list[Message] = []
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.query_handlers = query_handlers

    def handle(self, message: Message):
        self.queue.append(message)

        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.AbstractEvent):
                self.handle_event(message)
            elif isinstance(message, commands.AbstractCommand):
                self.handle_command(message)
            elif isinstance(message, queries.AbstractQuery):
                return self.handle_query(message)
            else:
                raise Exception(f"{message} was not an Event, Command or Query")

    def handle_event(self, event: events.AbstractEvent) -> None:
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f"Handling event {event} with handler {handler}")
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue

    def handle_command(self, command: commands.AbstractCommand) -> None:
        logger.debug(f"Handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise

    def handle_query(self, query: queries.AbstractQuery):
        logger.debug(f"Handling query {query}")
        try:
            handler = self.query_handlers[type(query)]
            results = handler(query)
            self.queue.extend(self.uow.collect_new_events())
            return results
        except Exception:
            logger.exception(f"Exception handling query {query}")
            raise
