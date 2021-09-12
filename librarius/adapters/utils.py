import typing as tp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from librarius.adapters.repository_contexts.sqlalchemy_implementation import SQLAlchemyContextMaker
from librarius.adapters.repositories.maker import RepositoryMaker
from librarius.adapters.repositories import PublicationsRepository

DEFAULT_SESSION_FACTORY: "sessionmaker" = sessionmaker(bind=create_engine("sqlite:///:memory:"))
DEFAULT_REPOSITORY_CONTEXT_FACTORY: "SQLAlchemyContextMaker" = SQLAlchemyContextMaker(DEFAULT_SESSION_FACTORY)
DEFAULT_REPOSITORY_FACTORY: "RepositoryMaker" = RepositoryMaker(PublicationsRepository)
