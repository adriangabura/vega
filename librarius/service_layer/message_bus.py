import logging
import typing as tp
from collections import deque
from librarius.domain.messages import (
    AbstractMessage,
    AbstractEvent,
    AbstractCommand,
    AbstractQuery,
)
from librarius.service_layer.uow import AbstractUnitOfWork
from librarius.domain.exceptions import SkipMessage

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: dict[tp.Type[AbstractEvent], list[tp.Callable]],
        command_handlers: dict[tp.Type[AbstractCommand], tp.Callable],
        query_handlers: dict[tp.Type[AbstractQuery], tp.Callable],
    ):
        self.queue: deque[AbstractMessage] = deque()
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.query_handlers = query_handlers

    def handle(self, message: AbstractMessage):
        self.queue.append(message)

        try:
            while self.queue:
                message = self.queue.popleft()
                if isinstance(message, AbstractEvent):
                    self.handle_event(message)
                elif isinstance(message, AbstractCommand):
                    self.handle_command(message)
                elif isinstance(message, AbstractQuery):
                    return self.handle_query(message)
                else:
                    raise Exception(f"{message} was not an Event, Command or Query")
        except SkipMessage as error:
            logger.warning(f"Skipping message {message.uuid} because {error.reason}")

    def handle_event(self, event: AbstractEvent) -> None:
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f"Handling event {event} with handler {handler}")
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception(f"Exception handling event {event}")
                continue

    def handle_command(self, command: AbstractCommand) -> None:
        logger.debug(f"Handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception(f"Exception handling command {command}")
            raise

    def handle_query(self, query: AbstractQuery):
        logger.debug(f"Handling query {query}")
        try:
            handler = self.query_handlers[type(query)]
            results = handler(query)
            self.queue.extend(self.uow.collect_new_events())
            return results
        except Exception:
            logger.exception(f"Exception handling query {query}")
            raise
