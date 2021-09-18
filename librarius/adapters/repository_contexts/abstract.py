import abc
import typing as tp

from librarius.utils import Map


TAbstractRepositoryContext = tp.TypeVar('TAbstractRepositoryContext', bound='AbstractRepositoryContext')


class AbstractRepositoryContext(abc.ABC, tp.Generic[TAbstractRepositoryContext]):
    session: tp.Any

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


TAbstractContextMaker = tp.TypeVar('TAbstractContextMaker', bound='AbstractContextMaker')


class AbstractContextMaker(abc.ABC, tp.Generic[TAbstractContextMaker, TAbstractRepositoryContext]):
    @abc.abstractmethod
    def __call__(self) -> "TAbstractRepositoryContext":
        raise NotImplementedError
