import typing as tp
import logging
from librarius.service_layer.handlers import AbstractCommandHandler
from librarius.domain.messages import commands
from librarius.domain import models
from librarius.service_layer import ensure

if tp.TYPE_CHECKING:
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
        series = models.Series(uuid=cmd.series_uuid, name=cmd.name)
        with self.uow as uow_context:
            ensure.series_not_exists_skip(cmd, uow_context)
            self.uow.repositories.series.add(series)
            self.uow.commit()


class AddAuthorToPublicationHandler(AbstractCommandHandler[commands.AddAuthorToPublication]):
    def __call__(self, cmd: 'commands.AddAuthorToPublication'):
        author = models.Author(uuid=cmd.author_uuid, name=cmd.author_name)
        with self.uow as uow_context:
            ensure.publication_exists(cmd, uow_context)


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


COMMAND_HANDLERS: tp.Mapping[tp.Type["AbstractCommand"], tp.Type["AbstractCommandHandler"]] = {
    commands.CreateAuthor: CreateAuthorHandler,
    commands.AddPublication: AddPublicationHandler,
    commands.RemovePublication: RemovePublicationHandler,
    commands.AddAuthorToPublication: AddAuthorToPublicationHandler,
    commands.CreateSeries: CreateSeriesHandler
}
