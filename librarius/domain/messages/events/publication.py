import dataclasses
from librarius.domain.messages import AbstractEvent


@dataclasses.dataclass
class PublicationAdded(AbstractEvent['PublicationAdded']):
    pass


@dataclasses.dataclass
class PublicationModified(AbstractEvent['PublicationModified']):
    pass


@dataclasses.dataclass
class PublicationRemoved(AbstractEvent['PublicationRemoved']):
    pass
