import abc
import typing as tp
from librarius.domain.messages import (
    TAbstractMessage,
    TAbstractCommand,
    TAbstractQuery,
    TAbstractEvent,
)

if tp.TYPE_CHECKING:
    from librarius.domain.messages import AbstractCommand, AbstractQuery, AbstractEvent
    from librarius.domain.models import Entity
    from librarius.service_layer.uow import TAbstractUnitOfWork

TAbstractHandler = tp.TypeVar("TAbstractHandler", bound="AbstractHandler")


class AbstractHandler(tp.Generic[TAbstractHandler, TAbstractMessage], abc.ABC):
    def __init__(self, uow: "TAbstractUnitOfWork"):
        self.uow = uow

    @abc.abstractmethod
    def __call__(self, message: "TAbstractMessage"):
        raise NotImplementedError


class AbstractCommandHandler(
    AbstractHandler["AbstractCommandHandler", TAbstractCommand],
    tp.Generic[TAbstractCommand],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, cmd: "TAbstractCommand") -> None:
        raise NotImplementedError


class AbstractEventHandler(
    AbstractHandler["AbstractEventHandler", TAbstractEvent],
    tp.Generic[TAbstractEvent],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, event: "TAbstractEvent") -> None:
        raise NotImplementedError


class AbstractQueryHandler(
    AbstractHandler["AbstractQueryHandler", TAbstractQuery],
    tp.Generic[TAbstractQuery],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(
        self, query: "TAbstractQuery"
    ) -> tp.Union[tp.Iterable["Entity"], "Entity"]:
        raise NotImplementedError
