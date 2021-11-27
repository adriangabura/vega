import typing as tp
from librarius.service.uow import AbstractUnitOfWork
from librarius.adapters.utils import (
    DEFAULT_REPOSITORY_CONTEXT_FACTORY,
    DEFAULT_REPOSITORY_FACTORY,
    DEFAULT_CASBIN_ENFORCER
)

if tp.TYPE_CHECKING:
    from casbin import Enforcer
    # from librarius.service.uow.abstract import TAbstractUnitOfWork
    from librarius.adapters.repositories.abstract import AbstractRepository
    from librarius.adapters.repositories.contexts import AbstractContextMaker
    from librarius.adapters.repositories.contexts import AbstractRepositoryContext
    from librarius.domain.messages import AbstractEvent
    from librarius.adapters.repositories.factory import DefaultRepositoryCollection


class GenericUnitOfWork(AbstractUnitOfWork["GenericUnitOfWork"]):
    def __init__(
        self,
        repository_factory=DEFAULT_REPOSITORY_FACTORY,
        context_factory: "AbstractContextMaker" = DEFAULT_REPOSITORY_CONTEXT_FACTORY,
        casbin_enforcer: "Enforcer" = DEFAULT_CASBIN_ENFORCER
    ):
        self.repository_factory: tp.Type["DefaultRepositoryCollection"] = repository_factory
        self.context_factory = context_factory
        self.casbin_enforcer = casbin_enforcer

    def __enter__(self, *args, **kwargs) -> "GenericUnitOfWork":
        self.context: "AbstractRepositoryContext" = self.context_factory()
        self.repositories: "DefaultRepositoryCollection" = self.repository_factory(
            self.context
        )
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
            for elem in repos[repo_name].touched:
                while elem.events:
                    yield elem.events.popleft()  # yield elem.events.pop(0)
