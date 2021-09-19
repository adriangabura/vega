import typing as tp
import logging

from librarius.domain.models import Publication, Author
from librarius.domain.messages import queries, AbstractQuery
from librarius.service_layer.handlers import AbstractQueryHandler
from librarius.service_layer.uow import SQLAlchemyUnitOfWork

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class RetrieveAllPublicationsHandler(AbstractQueryHandler[queries.AllPublications]):
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


class RetrieveAuthorByUuid(AbstractQueryHandler[queries.AuthorByUuid]):
    def __call__(self, query: 'queries.AuthorByUuid'):
        with self.uow as uow_context:
            session: 'Session' = self.uow.context.session
            result: "Author" = session.query(Author).filter_by(uuid=query.author_uuid).first()
            session.expunge_all()
            return result


QUERY_HANDLERS: tp.Mapping[tp.Type['AbstractQuery'], tp.Type["AbstractQueryHandler"]] = {
    queries.AllPublications: RetrieveAllPublicationsHandler,
    queries.AuthorByUuid: RetrieveAuthorByUuid
}
