import abc
import typing as tp

if tp.TYPE_CHECKING:
    from librarius.domain.messages import AbstractEvent
    from librarius.adapters.repositories.abstract import AbstractRepository
    from librarius.adapters.repositories.contexts.abstract import (
        TAbstractContextMaker,
        AbstractRepositoryContext,
    )
    from librarius.adapters.repositories.factory import AbstractRepositoryCollection
    from casbin import Enforcer


TAbstractUnitOfWork = tp.TypeVar("TAbstractUnitOfWork", bound="AbstractUnitOfWork")


class AbstractUnitOfWork(abc.ABC, tp.Generic[TAbstractUnitOfWork]):
    repositories: "AbstractRepositoryCollection"
    context: "AbstractRepositoryContext"
    casbin_enforcer: "Enforcer"

    @abc.abstractmethod
    def __init__(
        self, repository_factory, context_factory: "TAbstractContextMaker"
    ) -> None:
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
