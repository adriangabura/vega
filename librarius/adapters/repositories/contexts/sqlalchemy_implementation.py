import abc
import typing as tp
from librarius.adapters.repository_contexts.abstract import TAbstractRepositoryContext, AbstractRepositoryContext, AbstractContextMaker

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyRepositoryContext(AbstractRepositoryContext['SQLAlchemyRepositoryContext']):
    def __init__(self, session: "Session"):
        self.session: "Session" = session

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def add(self, model) -> None:
        self.session.add(model)

    def remove(self, model) -> None:
        self.session.delete(model)

    def close(self) -> None:
        self.session.close()


class SQLAlchemyContextMaker(AbstractContextMaker['SQLAlchemyContextMaker', 'SQLAlchemyRepositoryContext']):
    def __init__(self, session_factory: "sessionmaker"):
        self.session_factory = session_factory

    def __call__(self) -> "SQLAlchemyRepositoryContext":
        session: "Session" = self.session_factory()
        return SQLAlchemyRepositoryContext(session)
