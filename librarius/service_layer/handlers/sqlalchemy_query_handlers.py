import typing as tp
import logging

from librarius.domain.models import Publication
from librarius.domain import queries
from librarius.service_layer.uow import SQLAlchemyUnitOfWork

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.types import QueryHandler

logger = logging.getLogger(__name__)


def retrieve_all_publications(query: queries.AllPublications, uow: "SQLAlchemyUnitOfWork") -> list[Publication]:
    try:
        if not isinstance(uow, SQLAlchemyUnitOfWork):
            raise TypeError(f"Passed Type {type(uow)} instead of {SQLAlchemyUnitOfWork}")
        elif not isinstance(query, queries.AllPublications):
            raise TypeError(f"Passed Type {type(query)} instead of {queries.AllPublications}")
        else:
            with uow:
                session: "Session" = uow.context.session
                results: list["Publication"] = session.query(Publication).all()
                session.expunge_all()
                return results
    except TypeError as error:
        logger.exception(error)


QUERY_HANDLERS: dict[tp.Type["queries.AbstractQuery"], "QueryHandler"] = {
    queries.AllPublications: retrieve_all_publications
}
