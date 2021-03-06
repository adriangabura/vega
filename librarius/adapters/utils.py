import dataclasses
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from librarius.adapters.repositories.contexts.sqlalchemy_implementation import (
    SQLAlchemyContextMaker,
)
from librarius.adapters.repositories.factory import DefaultRepositoryCollection
from librarius.entrypoints.app_enforcer import get_enforcer

DEFAULT_SESSION_FACTORY: "sessionmaker" = sessionmaker(
    bind=create_engine("sqlite:///test.db")
)
DEFAULT_REPOSITORY_CONTEXT_FACTORY: "SQLAlchemyContextMaker" = SQLAlchemyContextMaker(
    DEFAULT_SESSION_FACTORY
)
DEFAULT_REPOSITORY_FACTORY = DefaultRepositoryCollection

DEFAULT_CASBIN_ENFORCER = get_enforcer()