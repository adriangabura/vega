import abc
import typing as tp

if tp.TYPE_CHECKING:
    from librarius.types import Message
    from librarius.domain import commands, events, queries
    from librarius.domain.models import Entity
    from librarius.service_layer.uow import AbstractUnitOfWork


class AbstractHandler(abc.ABC):
    def __init__(self, uow: "AbstractUnitOfWork"):
        self.uow = uow

    @abc.abstractmethod
    def __call__(self, message: "Message"):
        raise NotImplementedError


class AbstractCommandHandler(AbstractHandler, abc.ABC):
    @abc.abstractmethod
    def __call__(self, cmd: "commands.AbstractCommand") -> tp.NoReturn:
        raise NotImplementedError


class AbstractEventHandler(AbstractHandler, abc.ABC):
    @abc.abstractmethod
    def __call__(self, event: "events.AbstractEvent") -> tp.NoReturn:
        raise NotImplementedError


class AbstractQueryHandler(AbstractHandler, abc.ABC):
    @abc.abstractmethod
    def __call__(self, query: "queries.AbstractQuery") -> tp.Union[tp.Iterable["Entity"], "Entity"]:
        raise NotImplementedError
