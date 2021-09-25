import typing as tp
import abc
from dataclasses import dataclass, fields
from librarius.adapters.repositories.contexts import AbstractRepositoryContext
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.publications import PublicationsRepository
from librarius.adapters.repositories.authors import AuthorsRepository
from librarius.adapters.repositories.series import SeriesRepository

TAbstractRepositoryCollection = tp.TypeVar('TAbstractRepositoryCollection', bound='AbstractRepositoryCollection')


class AbstractRepositoryCollection(tp.Generic[TAbstractRepositoryCollection], abc.ABC):
    _context: AbstractRepositoryContext
    publications: PublicationsRepository
    authors: AuthorsRepository
    series: SeriesRepository

    def __iter__(self) -> tp.Generator[str, None, None]:
        for key in self._asdict():
            yield key

    def __getitem__(self, item: str) -> AbstractRepository:
        return self._asdict()[item]

    def inject_context(self, repository: tp.Type[AbstractRepository]) -> None:
        instance = repository(self._context)
        object.__setattr__(self, repository.name, instance)

    @abc.abstractmethod
    def _asdict(self) -> dict[str, AbstractRepository]:
        raise NotImplementedError


@dataclass(frozen=True)
class DefaultRepositoryCollection(AbstractRepositoryCollection['DefaultRepositoryCollection']):
    publications: PublicationsRepository
    authors: AuthorsRepository
    series: SeriesRepository

    def __init__(self, context: AbstractRepositoryContext):
        object.__setattr__(self, '_context', context)
        self.inject_context(PublicationsRepository)
        self.inject_context(AuthorsRepository)
        self.inject_context(SeriesRepository)

    def _asdict(self) -> dict[str, AbstractRepository]:
        return {i.name: self.__dict__[i.name] for i in fields(self)}
