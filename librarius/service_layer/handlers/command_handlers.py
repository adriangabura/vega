import typing as tp
import logging
from librarius.service_layer.handlers import AbstractCommandHandler
from librarius.domain.messages import commands
from librarius.domain import models
from librarius.service_layer import ensure
from librarius.service_layer.ensure import exceptions

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.domain.messages import AbstractCommand

logger = logging.getLogger(__name__)


class CreateAuthorHandler(AbstractCommandHandler[commands.CreateAuthor]):
    def __call__(self, cmd: 'commands.CreateAuthor'):
        author = models.Author(uuid=cmd.author_uuid, name=cmd.name)
        with self.uow as uow_context:
            ensure.author_not_exists_skip(cmd, uow_context)
            self.uow.repositories.authors.add(author)
            self.uow.commit()


class CreateSeriesHandler(AbstractCommandHandler[commands.CreateSeries]):
    def __call__(self, cmd: 'commands.CreateSeries'):
        series = models.Series(uuid=cmd.series_uuid, name=cmd.series_name)
        with self.uow as uow_context:
            ensure.series_not_exists_skip(cmd, uow_context)
            self.uow.repositories.series.add(series)
            self.uow.commit()


class AddAuthorToPublicationHandler(AbstractCommandHandler[commands.AddAuthorToPublication]):
    def __call__(self, cmd: 'commands.AddAuthorToPublication'):
        #author = models.Author(uuid=cmd.author_uuid, name=cmd.author_name)
        with self.uow as uow_context:
            ensure.publication_exists(cmd, uow_context)

        try:
            with self.uow as uow_context:
                ensure.author_exists(cmd, uow_context)
        except exceptions.AuthorNotFound as error:
            logger.exception(error)
            create_author = CreateAuthorHandler(self.uow)
            create_author(commands.CreateAuthor(name=cmd.author_name, author_uuid=cmd.author_uuid))
        with self.uow as uow_context:
            session: 'Session' = self.uow.context.session
            author = session.query(models.Author).filter_by(uuid=cmd.author_uuid).first()
            publication = session.query(models.Publication).filter_by(uuid=cmd.publication_uuid).first()
            publication.add_author(author)
            self.uow.commit()


class AddPublicationHandler(AbstractCommandHandler[commands.AddPublication]):
    def __call__(self, cmd: 'commands.AddPublication'):
        publication = models.Publication(title=cmd.title, uuid=cmd.publication_uuid)
        with self.uow as uow_context:
            #ensure.publication_not_exists(cmd, uow_context)
            ensure.publication.publication_skip_exists(cmd, uow_context)
            publication.add_publication()
            uow_context.repositories.publications.add(publication)
            uow_context.commit()


class RemovePublicationHandler(AbstractCommandHandler[commands.RemovePublication]):
    def __call__(self, cmd: 'commands.RemovePublication'):
        pass


class AddPublicationToSeriesHandler(AbstractCommandHandler[commands.AddPublicationToSeries]):
    def __call__(self, cmd: 'commands.AddPublicationToSeries'):
        with self.uow as uow_context:
            ensure.publication_exists(cmd, uow_context)

        try:
            with self.uow as uow_context:
                ensure.series_exists(cmd, uow_context)
        except exceptions.SeriesNotFound as error:
            logger.exception(error)
            create_series = CreateSeriesHandler(self.uow)
            create_series(commands.CreateSeries(cmd.series_uuid, cmd.series_name))
        with self.uow as uow_context:
            session: 'Session' = self.uow.context.session
            publication = session.query(models.Publication).filter_by(uuid=cmd.publication_uuid).first()
            series = session.query(models.Series).filter_by(uuid=cmd.series_uuid).first()
            series.add_publication(publication)
            self.uow.commit()


COMMAND_HANDLERS: tp.Mapping[tp.Type["AbstractCommand"], tp.Type["AbstractCommandHandler"]] = {
    commands.CreateAuthor: CreateAuthorHandler,
    commands.AddPublication: AddPublicationHandler,
    commands.RemovePublication: RemovePublicationHandler,
    commands.AddAuthorToPublication: AddAuthorToPublicationHandler,
    commands.CreateSeries: CreateSeriesHandler,
    commands.AddPublicationToSeries: AddPublicationToSeriesHandler
}
