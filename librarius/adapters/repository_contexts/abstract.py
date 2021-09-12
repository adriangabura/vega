import abc
import typing as tp

from librarius.utils import Map

if tp.TYPE_CHECKING:
    from librarius.adapters.repositories import AbstractRepository


class AbstractRepositoryContext(abc.ABC):
    session: tp.Optional[tp.Any]

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, model) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, model) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class AbstractContextMaker(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> "AbstractRepositoryContext":
        raise NotImplementedError
