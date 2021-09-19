import typing as tp
import logging

from librarius.domain.models import Publication
from librarius.domain.messages import queries, AbstractQuery
from librarius.service_layer.handlers import AbstractQueryHandler
from librarius.service_layer.uow import SQLAlchemyUnitOfWork

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class RetrieveAllPublications(AbstractQueryHandler[queries.AllPublications]):
    def __call__(self, query: 'queries.AllPublications'):
        try:
            if not isinstance(query, queries.AllPublications):
                raise TypeError(f"Passed Type {type(query)} instead of {queries.AllPublications}")
            else:
                with self.uow:
                    session: 'Session' = self.uow.context.session
                    results: list['Publication'] = session.query(Publication).all()
                    session.expunge_all()
                    return results
        except TypeError as error:
            logger.exception(error)


QUERY_HANDLERS: tp.Mapping[tp.Type['AbstractQuery'], tp.Type["AbstractQueryHandler"]] = {
    queries.AllPublications: RetrieveAllPublications
}
