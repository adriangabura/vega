import typing as tp
from librarius.service_layer.uow import AbstractUnitOfWork
from librarius.adapters.utils import DEFAULT_REPOSITORY_CONTEXT_FACTORY, DEFAULT_REPOSITORY_FACTORY


if tp.TYPE_CHECKING:
    #from librarius.service_layer.uow.abstract import TAbstractUnitOfWork
    from librarius.adapters.repositories.abstract import AbstractRepository
    from librarius.adapters.repositories.contexts import AbstractContextMaker
    from librarius.adapters.repositories.contexts import AbstractRepositoryContext
    from librarius.domain.messages import AbstractEvent
    from librarius.adapters.repositories.factory import DefaultRepositoryCollection


class SQLAlchemyUnitOfWork(AbstractUnitOfWork["SQLAlchemyUnitOfWork"]):
    def __init__(self,
                 repository_factory = DEFAULT_REPOSITORY_FACTORY,
                 context_factory: "AbstractContextMaker" = DEFAULT_REPOSITORY_CONTEXT_FACTORY):
        self.repository_factory: tp.Type[DefaultRepositoryCollection] = repository_factory
        self.context_factory = context_factory

    def __enter__(self, *args, **kwargs) -> "SQLAlchemyUnitOfWork":
        self.context: "AbstractRepositoryContext" = self.context_factory()
        self.repositories: DefaultRepositoryCollection = self.repository_factory(self.context)
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.context.rollback()
        self.context.close()

    def commit(self) -> None:
        self.context.commit()

    def rollback(self) -> None:
        self.context.rollback()

    def collect_new_events(self) -> tp.Generator["AbstractEvent", None, None]:
        repos = self.repositories
        for repo_name in repos:
            for elem in repos[repo_name].seen:
                while elem.events:
                    yield elem.events.pop(0)
