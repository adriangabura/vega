import typing as tp
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from librarius.adapters.orm import metadata, start_mappers
from librarius.adapters.repositories.contexts.sqlalchemy_implementation import SQLAlchemyContextMaker


@pytest.fixture(scope="session")
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture(scope="session")
def mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture(scope="session")
def sql_alchemy_context_factory(sqlite_session_factory: "sessionmaker") -> tp.Iterator["SQLAlchemyContextMaker"]:
    yield SQLAlchemyContextMaker(sqlite_session_factory)
