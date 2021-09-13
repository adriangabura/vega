import abc
import typing as tp
from librarius.adapters.repository_contexts import AbstractRepositoryContext, AbstractContextMaker

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyRepositoryContext(AbstractRepositoryContext):
    def __init__(self, session: "Session"):
        self.session = session

    def commit(self) -> tp.NoReturn:
        self.session.commit()

    def rollback(self) -> tp.NoReturn:
        self.session.rollback()

    def add(self, model) -> tp.NoReturn:
        self.session.add(model)

    def remove(self, model) -> tp.NoReturn:
        self.session.delete(model)

    def close(self) -> tp.NoReturn:
        self.session.close()


class SQLAlchemyContextMaker(AbstractContextMaker):
    def __init__(self, session_factory: "sessionmaker"):
        self.session_factory = session_factory

    def __call__(self) -> "SQLAlchemyRepositoryContext":
        session: "Session" = self.session_factory()
        return SQLAlchemyRepositoryContext(session)
