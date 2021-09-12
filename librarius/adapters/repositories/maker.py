import typing as tp
from librarius.utils import Map
from librarius.adapters.repositories import AbstractRepositoryMaker

if tp.TYPE_CHECKING:
    from librarius.adapters.repositories import AbstractRepository
    from librarius.adapters.repository_contexts import AbstractRepositoryContext


class RepositoryMaker(AbstractRepositoryMaker):
    def __init__(self, *args: tp.Type["AbstractRepository"]):
        self._repositories = args

    def __call__(self, context: "AbstractRepositoryContext") -> "Map[str, AbstractRepository]":
        return Map({repository.name: repository(context) for repository in self._repositories})
