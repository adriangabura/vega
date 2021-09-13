import typing as tp
import logging
from librarius.domain import events

if tp.TYPE_CHECKING:
    from librarius.types import EventHandler
    from librarius.service_layer.uow import AbstractUnitOfWork

logger = logging.getLogger(__name__)


def publication_added(event: "events.PublicationAdded", uow: "AbstractUnitOfWork"):
    print("ADDED")


EVENT_HANDLERS: tp.Mapping[tp.Type["events.AbstractEvent"], tp.Sequence["EventHandler"]] = {
    events.PublicationAdded: [publication_added],
    events.PublicationModified: [],
    events.PublicationRemoved: []
}
