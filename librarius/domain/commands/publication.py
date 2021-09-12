import dataclasses
from uuid import UUID
from librarius.domain.commands import AbstractCommand


@dataclasses.dataclass
class AddPublication(AbstractCommand):
    title: str
    uuid: str


@dataclasses.dataclass
class ModifyPublication(AbstractCommand):
    pass


@dataclasses.dataclass
class RemovePublication(AbstractCommand):
    pass
