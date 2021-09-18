import abc
import typing as tp

from librarius.utils import Map

if tp.TYPE_CHECKING:
    from librarius.domain.messages.events import AbstractEvent
    from librarius.adapters.repositories.abstract import AbstractRepository, TAbstractRepositoryMaker
    from librarius.adapters.repository_contexts.abstract import TAbstractContextMaker, AbstractRepositoryContext


TAbstractUnitOfWork = tp.TypeVar('TAbstractUnitOfWork', bound='AbstractUnitOfWork')


class AbstractUnitOfWork(abc.ABC, tp.Generic[TAbstractUnitOfWork]):
    repositories: "Map[str, AbstractRepository]"
    context: "AbstractRepositoryContext"

    @abc.abstractmethod
    def __init__(self,
                 repository_factory: "TAbstractRepositoryMaker",
                 context_factory: "TAbstractContextMaker") -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __enter__(self, *args, **kwargs) -> "TAbstractUnitOfWork":
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def collect_new_events(self) -> tp.Generator["AbstractEvent", None, None]:
        raise NotImplementedError
