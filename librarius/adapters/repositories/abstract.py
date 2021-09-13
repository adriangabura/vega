import abc
import typing as tp

if tp.TYPE_CHECKING:
    from librarius.adapters.repository_contexts import AbstractRepositoryContext
    from librarius.utils import Map


class AbstractRepository(abc.ABC):
    name: tp.ClassVar[str] = "abstract"

    def __init__(self, context: "AbstractRepositoryContext"):
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


class AbstractRepositoryMaker(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args: tp.Type["AbstractRepository"]):
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, context: "AbstractRepositoryContext") -> "Map[str, AbstractRepository]":
        raise NotImplementedError
