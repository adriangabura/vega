import dataclasses
from librarius.domain.events import AbstractEvent


@dataclasses.dataclass
class PublicationAdded(AbstractEvent):
    pass


@dataclasses.dataclass
class PublicationModified(AbstractEvent):
    pass


@dataclasses.dataclass
class PublicationRemoved(AbstractEvent):
    pass
