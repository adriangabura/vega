import typing as tp
import logging
from librarius.service_layer.handlers import AbstractCommandHandler
from librarius.domain.messages import commands
from librarius.domain import models

if tp.TYPE_CHECKING:
    from librarius.domain.messages import AbstractCommand

logger = logging.getLogger(__name__)


class AddAuthorToPublicationHandler(AbstractCommandHandler[commands.AddAuthor]):
    def __call__(self, cmd: 'commands.AddAuthorToPublication'):
        with self.uow as uow:
            pass


class AddPublicationHandler(AbstractCommandHandler[commands.AddPublication]):
    def __call__(self, cmd: 'commands.AddPublication'):
        with self.uow:
            # publication = uow.repositories.publication.find(cmd.uuid)
            # if publication is None:
            #    publication = models.Publication()
            #    uow.repositories.publication.add(publication)
            publication = models.Publication(title=cmd.title, uuid=cmd.uuid)
            publication.add_publication()
            self.uow.repositories.publications.add(publication)
            self.uow.commit()


class RemovePublicationHandler(AbstractCommandHandler[commands.RemovePublication]):
    def __call__(self, cmd: 'commands.RemovePublication'):
        pass


COMMAND_HANDLERS: tp.Mapping[tp.Type["AbstractCommand"], tp.Type["AbstractCommandHandler"]] = {
    commands.AddPublication: AddPublicationHandler,
    commands.RemovePublication: RemovePublicationHandler,
    commands.AddAuthorToPublication: AddAuthorToPublicationHandler
}
