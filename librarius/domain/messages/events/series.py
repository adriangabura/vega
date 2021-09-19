import dataclasses
from librarius.domain.messages import AbstractEvent


@dataclasses.dataclass
class PublicationAddedToSeries(AbstractEvent['PublicationAddedToSeries']):
    pass

