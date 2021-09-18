import abc
import typing as tp

from librarius.adapters.repositories.contexts import TAbstractRepositoryContext

if tp.TYPE_CHECKING:
    from librarius.utils import Map


TAbstractRepository = tp.TypeVar('TAbstractRepository', bound='AbstractRepository')


class AbstractRepository(abc.ABC, tp.Generic[TAbstractRepository, TAbstractRepositoryContext]):
    name: tp.ClassVar[str] = "abstract.py"

    def __init__(self, context: "TAbstractRepositoryContext"):
        self.context = context
        self.seen: set = set()

    @abc.abstractmethod
    def add(self, model):
        self.context.add(model)

    @abc.abstractmethod
    def remove(self, model):
        self.context.remove(model)

    @abc.abstractmethod
    def find(self):
        pass


# TAbstractRepositoryMaker = tp.TypeVar('TAbstractRepositoryMaker', bound='AbstractRepositoryMaker')
#
#
# class AbstractRepositoryMaker(abc.ABC,
#                               tp.Generic[TAbstractRepositoryMaker, TAbstractRepository, TAbstractRepositoryContext]):
#     @abc.abstractmethod
#     def __init__(self, *args: tp.Type["TAbstractRepository"]):
#         raise NotImplementedError
#
#     @abc.abstractmethod
#     def __call__(self, context: "TAbstractRepositoryContext") -> "Map[str, TAbstractRepository]":
#         raise NotImplementedError
