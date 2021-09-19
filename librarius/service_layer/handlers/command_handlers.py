import typing as tp
import logging
from librarius.service_layer.handlers import AbstractCommandHandler
from librarius.domain.messages import commands
from librarius.domain import models
from librarius.service_layer import ensure

if tp.TYPE_CHECKING:
    from librarius.domain.messages import AbstractCommand

logger = logging.getLogger(__name__)


class AddAuthorToPublicationHandler(AbstractCommandHandler[commands.AddAuthorToPublication]):
    def __call__(self, cmd: 'commands.AddAuthorToPublication'):
        with self.uow as uow:
            pass


class AddPublicationHandler(AbstractCommandHandler[commands.AddPublication]):
    def __call__(self, cmd: 'commands.AddPublication'):
        publication = models.Publication(title=cmd.title, uuid=cmd.uuid)
        with self.uow as uow_context:
            ensure.publication_not_exists(cmd, uow_context)
            
            publication.add_publication()
            uow_context.repositories.publications.add(publication)
            uow_context.commit()


class RemovePublicationHandler(AbstractCommandHandler[commands.RemovePublication]):
    def __call__(self, cmd: 'commands.RemovePublication'):
        pass


COMMAND_HANDLERS: tp.Mapping[tp.Type["AbstractCommand"], tp.Type["AbstractCommandHandler"]] = {
    commands.AddPublication: AddPublicationHandler,
    commands.RemovePublication: RemovePublicationHandler,
    commands.AddAuthorToPublication: AddAuthorToPublicationHandler
}
