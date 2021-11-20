import typing as tp
import logging
from librarius.service.handlers import AbstractCommandHandler
from librarius.domain.messages import commands
from librarius.domain import models
from librarius.service import ensure
from librarius.service.ensure import exceptions

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from librarius.domain.messages import AbstractCommand

logger = logging.getLogger(__name__)


class CreateAuthorHandler(AbstractCommandHandler[commands.CreateAuthor]):
    def __call__(self, cmd: "commands.CreateAuthor"):
        with self.uow:
            author = self.uow.repositories.authors.find_by_uuid(cmd.author_uuid)
            if author is None:
                author = models.Author(uuid=cmd.author_uuid, name=cmd.name)
                self.uow.repositories.authors.add(author)
            self.uow.commit()


class CreateSeriesHandler(AbstractCommandHandler[commands.CreateSeries]):
    def __call__(self, cmd: "commands.CreateSeries"):
        with self.uow:
            series = self.uow.repositories.series.find_by_uuid(cmd.series_uuid)
            if series is not None:
                logger.warning("Series exists!")
            else:
                series = models.Series(uuid=cmd.series_uuid, name=cmd.series_name)
                self.uow.repositories.series.add(series)
            self.uow.commit()
            # Consider returns!


class AddAuthorToPublicationHandler(
    AbstractCommandHandler[commands.AddAuthorToPublication]
):
    def __call__(self, cmd: "commands.AddAuthorToPublication"):
        with self.uow:
            publication = self.uow.repositories.publications.find_by_uuid(
                cmd.author_uuid
            )

            if publication is not None:
                author = self.uow.repositories.authors.find_by_uuid(cmd.author_uuid)
                if author is None:
                    author = models.Author(uuid=cmd.author_uuid, name=cmd.author_name)

                publication.add_author(author)

                # Maybe return result?
            else:
                pass
                # Maybe return result?
            self.uow.commit()


class AddPublicationHandler(AbstractCommandHandler[commands.CreatePublication]):
    def __call__(self, cmd: "commands.CreatePublication"):
        with self.uow:
            publication = self.uow.repositories.publications.find_by_uuid(
                cmd.publication_uuid
            )

            if publication is None:
                publication = models.Publication(
                    title=cmd.title, uuid=cmd.publication_uuid
                )
            self.uow.repositories.publications.add(publication)

            self.uow.commit()

            # Consider returning results!!!


class RemovePublicationHandler(AbstractCommandHandler[commands.RemovePublication]):
    def __call__(self, cmd: "commands.RemovePublication"):
        pass


class AddPublicationToSeriesHandler(
    AbstractCommandHandler[commands.AddPublicationToSeries]
):
    def __call__(self, cmd: "commands.AddPublicationToSeries"):
        with self.uow:
            series = self.uow.repositories.series.find_by_uuid(cmd.series_uuid)
            if series is not None:
                publication = self.uow.repositories.publications.find_by_uuid(
                    cmd.publication_uuid
                )
                if publication is not None:
                    series.add_publication(publication)
                else:
                    logger.warning("No such publication exists!")

            self.uow.commit()
            # Consider returning results!


COMMAND_HANDLERS: tp.Mapping[
    tp.Type["AbstractCommand"], tp.Type["AbstractCommandHandler"]
] = {
    commands.CreateAuthor: CreateAuthorHandler,
    commands.CreatePublication: AddPublicationHandler,
    commands.RemovePublication: RemovePublicationHandler,
    commands.AddAuthorToPublication: AddAuthorToPublicationHandler,
    commands.CreateSeries: CreateSeriesHandler,
    commands.AddPublicationToSeries: AddPublicationToSeriesHandler,
}