import dataclasses
from uuid import UUID
from librarius.domain.queries import AbstractQuery


@dataclasses.dataclass
class AllPublications(AbstractQuery):
    pass


@dataclasses.dataclass
class AddPublication(AbstractQuery):
    title: str
