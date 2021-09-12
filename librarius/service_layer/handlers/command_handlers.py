import typing as tp
import logging
from librarius.domain import commands
from librarius.domain import models

if tp.TYPE_CHECKING:
    from librarius.types import CommandHandler
    from librarius.service_layer.uow import AbstractUnitOfWork

logger = logging.getLogger(__name__)


def add_author(cmd: "commands.AddAuthor", uow: "AbstractUnitOfWork"):
    with uow:
        pass


def add_publication(cmd: "commands.AddPublication", uow: "AbstractUnitOfWork"):
    with uow:
        #publication = uow.repositories.publication.find(cmd.uuid)
        #if publication is None:
        #    publication = models.Publication()
        #    uow.repositories.publication.add(publication)
        publication = models.Publication(title=cmd.title, uuid=cmd.uuid)
        publication.add_publication()
        uow.repositories.publications.add(publication)
        uow.commit()


def remove_publication(cmd: "commands.RemovePublication", uow: "AbstractUnitOfWork"):
    pass


COMMAND_HANDLERS: dict[tp.Type["commands.AbstractCommand"], "CommandHandler"] = {
    commands.AddPublication: add_publication,
    commands.RemovePublication: remove_publication
}
