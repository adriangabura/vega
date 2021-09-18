import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class AllPublications(AbstractQuery['AllPublications']):
    pass


@dataclasses.dataclass
class AddPublication(AbstractQuery['AddPublication']):
    title: str
