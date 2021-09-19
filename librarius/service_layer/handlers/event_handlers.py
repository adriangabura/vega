import typing as tp
import logging
from librarius.domain.messages import events, AbstractEvent
from librarius.service_layer.handlers import AbstractEventHandler

logger = logging.getLogger(__name__)


class PublicationAddedHandler(AbstractEventHandler[events.PublicationAdded]):
    def __call__(self, event: 'events.PublicationAdded'):
        logger.info('Publication added')


class AuthorAddedHandler(AbstractEventHandler[events.AuthorAdded]):
    def __call__(self, event: 'events.AuthorAdded'):
        logger.info('Author added')


EVENT_HANDLERS: tp.Mapping[tp.Type["AbstractEvent"], tp.Sequence[tp.Type[AbstractEventHandler]]] = {
    events.PublicationAdded: [PublicationAddedHandler],
    events.PublicationModified: [],
    events.PublicationRemoved: [],
    events.AuthorAdded: [AuthorAddedHandler]
}
