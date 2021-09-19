import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class AllAuthors(AbstractQuery['AllAuthors']):
    pass


@dataclasses.dataclass
class AuthorByUuid(AbstractQuery['AuthorByUuid']):
    author_uuid: str
