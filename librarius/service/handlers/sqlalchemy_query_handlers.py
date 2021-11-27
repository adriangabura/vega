import typing as tp
import logging

from librarius.domain import models
from librarius.domain.models import Publication, Author, Series
from librarius.domain.messages import queries, AbstractQuery
from librarius.service.handlers import AbstractQueryHandler
from librarius.service.uow import GenericUnitOfWork

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class RetrieveAllPublicationsHandler(AbstractQueryHandler[queries.AllPublications]):
    def __call__(self, query: "queries.AllPublications"):
        try:
            if not isinstance(query, queries.AllPublications):
                raise TypeError(
                    f"Passed Type {type(query)} instead of {queries.AllPublications}"
                )
            else:
                with self.uow:
                    session: "Session" = self.uow.context.session
                    results: list["Publication"] = session.query(Publication).all()
                    session.expunge_all()
                    return results
        except TypeError as error:
            logger.exception(error)


class RetrieveResourceByName(AbstractQueryHandler[queries.ResourceByName]):
    def __call__(self, query: "queries.ResourceByName"):
        with self.uow:
            session: "Session" = self.uow.context.session
            result: "models.Resource" = session.query(models.Resource).filter_by(name=query.resource_name).first()
            session.expunge_all()
            return result


class RetrieveRoleByName(AbstractQueryHandler[queries.RoleByName]):
    def __call__(self, query: "queries.RoleByName"):
        with self.uow:
            session: "Session" = self.uow.context.session
            result: "models.Role" = session.query(models.Role).filter_by(name=query.role_name).first()
            session.expunge_all()
            return result


class RetrieveUserByUsername(AbstractQueryHandler[queries.UserByUsername]):
    def __call__(self, query: "queries.UserByUsername"):
        with self.uow:
            session: "Session" = self.uow.context.session
            result: "models.User" = session.query(models.User).filter_by(name=query.username).first()
            session.expunge_all()
            return result



class RetrieveAuthorByUuid(AbstractQueryHandler[queries.AuthorByUuid]):
    def __call__(self, query: "queries.AuthorByUuid"):
        with self.uow as uow_context:
            session: "Session" = self.uow.context.session
            result: "Author" = (
                session.query(Author).filter_by(uuid=query.author_uuid).first()
            )
            session.expunge_all()
            return result


class RetrieveAllAuthors(AbstractQueryHandler[queries.AllAuthors]):
    def __call__(self, query: "queries.AllAuthors"):
        with self.uow as uow_context:
            session: "Session" = self.uow.context.session
            result: list["Author"] = session.query(Author).all()
            session.expunge_all()
            return result


class RetrieveSeriesByUuid(AbstractQueryHandler[queries.SeriesByUuid]):
    def __call__(self, query: "queries.SeriesByUuid"):
        with self.uow as uow_context:
            session: "Session" = self.uow.context.session
            result: "Series" = (
                session.query(Series).filter_by(uuid=query.series_uuid).first()
            )
            session.expunge_all()
            return result


class RetrievePublicationByUuid(AbstractQueryHandler[queries.PublicationByUuid]):
    def __call__(self, query: "queries.PublicationByUuid"):
        with self.uow as uow_context:
            session: "Session" = self.uow.context.session
            result: "Publication" = (
                session.query(Publication)
                .filter_by(uuid=query.publication_uuid)
                .first()
            )
            session.expunge_all()
            return result


QUERY_HANDLERS: tp.Mapping[
    tp.Type["AbstractQuery"], tp.Type["AbstractQueryHandler"]
] = {
    queries.UserByUsername: RetrieveUserByUsername,
    queries.RoleByName: RetrieveRoleByName,
    queries.ResourceByName: RetrieveResourceByName,
    queries.AllPublications: RetrieveAllPublicationsHandler,
    queries.PublicationByUuid: RetrievePublicationByUuid,
    queries.AuthorByUuid: RetrieveAuthorByUuid,
    queries.AllAuthors: RetrieveAllAuthors,
    queries.SeriesByUuid: RetrieveSeriesByUuid,
}
