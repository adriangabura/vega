import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class AllPublications(AbstractQuery['AllPublications']):
    pass


@dataclasses.dataclass
class PublicationByUuid(AbstractQuery['AllPublications']):
    publication_uuid: str
