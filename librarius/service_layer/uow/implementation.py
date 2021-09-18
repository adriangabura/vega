import typing as tp
from librarius.service_layer.uow import AbstractUnitOfWork
from librarius.adapters.utils import DEFAULT_REPOSITORY_CONTEXT_FACTORY, DEFAULT_REPOSITORY_FACTORY
from librarius.utils import Map
#from librarius.service_layer.uow.abstract import TAbstractUnitOfWork

if tp.TYPE_CHECKING:
    #from librarius.service_layer.uow.abstract import TAbstractUnitOfWork
    from librarius.adapters.repositories import AbstractRepository
    from librarius.adapters.repositories.maker import AbstractRepositoryMaker
    from librarius.adapters.repository_contexts import AbstractContextMaker
    from librarius.adapters.repository_contexts import AbstractRepositoryContext
    from librarius.domain.messages.events import AbstractEvent


class SQLAlchemyUnitOfWork(AbstractUnitOfWork["SQLAlchemyUnitOfWork"]):
    def __init__(self,
                 repository_factory: "AbstractRepositoryMaker" = DEFAULT_REPOSITORY_FACTORY,
                 context_factory: "AbstractContextMaker" = DEFAULT_REPOSITORY_CONTEXT_FACTORY):
        self.repository_factory = repository_factory
        self.context_factory = context_factory

    def __enter__(self, *args, **kwargs) -> "SQLAlchemyUnitOfWork":
        self.context: "AbstractRepositoryContext" = self.context_factory()
        self.repositories: "Map[str, AbstractRepository]" = self.repository_factory(self.context)
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.context.rollback()
        self.context.close()

    def commit(self) -> None:
        self.context.commit()

    def rollback(self) -> None:
        self.context.rollback()

    def collect_new_events(self) -> tp.Generator["AbstractEvent", None, None]:
        for reponame in self.repositories:
            for elem in self.repositories[reponame].seen:
                while elem.events:
                    yield elem.events.pop(0)
