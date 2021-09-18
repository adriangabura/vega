import typing as tp
import logging
from librarius.domain.messages import events, AbstractEvent
from librarius.service_layer.handlers import AbstractEventHandler

logger = logging.getLogger(__name__)


class PublicationAdded(AbstractEventHandler[events.PublicationAdded]):
    def __call__(self, event: 'AbstractEvent'):
        print("ADDED")


EVENT_HANDLERS: tp.Mapping[tp.Type["AbstractEvent"], tp.Sequence["AbstractEventHandler"]] = {
    events.PublicationAdded: [PublicationAdded],
    events.PublicationModified: [],
    events.PublicationRemoved: []
}
