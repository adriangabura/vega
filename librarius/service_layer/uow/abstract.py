import abc
import typing as tp

from librarius.utils import Map

if tp.TYPE_CHECKING:
    from librarius.domain.events import AbstractEvent
    from librarius.adapters.repositories import AbstractRepository, AbstractRepositoryMaker
    from librarius.adapters.repository_contexts import AbstractContextMaker


class AbstractUnitOfWork(abc.ABC):
    repositories: "Map[str, AbstractRepository]"

    @abc.abstractmethod
    def __init__(self,
                 repository_factory: "AbstractRepositoryMaker",
                 context_factory: "AbstractContextMaker") -> tp.NoReturn:
        raise NotImplementedError

    @abc.abstractmethod
    def __enter__(self, *args, **kwargs) -> "AbstractUnitOfWork":
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args, **kwargs) -> tp.NoReturn:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> tp.NoReturn:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> tp.NoReturn:
        raise NotImplementedError

    @abc.abstractmethod
    def collect_new_events(self) -> tp.Generator["AbstractEvent", None, None]:
        raise NotImplementedError
