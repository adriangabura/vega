import typing as tp
import pathlib
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from librarius.adapters.orm import metadata, start_mappers
from librarius.adapters.repositories.contexts.sqlalchemy_implementation import (
    SQLAlchemyContextMaker,
)


@pytest.fixture(scope="session")
def in_memory_sqlite_db():
    file_name = "sqlite_test.db"
    engine = create_engine(f"sqlite:///tests/{file_name}")
    metadata.create_all(engine)
    yield engine
    path = pathlib.Path(__file__).parent.parent / file_name
    path.unlink()


@pytest.fixture(scope="session")
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture(scope="module")
def mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture(scope="session")
def sql_alchemy_context_factory(
    sqlite_session_factory: "sessionmaker",
) -> tp.Iterator["SQLAlchemyContextMaker"]:
    yield SQLAlchemyContextMaker(sqlite_session_factory)
