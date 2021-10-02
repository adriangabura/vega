import abc
import typing as tp

from librarius.adapters.repositories.contexts import TAbstractRepositoryContext


TAbstractRepository = tp.TypeVar('TAbstractRepository', bound='AbstractRepository')


class AbstractRepository(abc.ABC, tp.Generic[TAbstractRepository, TAbstractRepositoryContext]):
    name: tp.ClassVar[str] = "abstract"

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
        raise NotImplementedError
