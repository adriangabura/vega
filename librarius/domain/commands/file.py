import typing as tp
import dataclasses
from uuid import UUID
from librarius.domain.commands import AbstractCommand


@dataclasses.dataclass
class StoreFile(AbstractCommand):
    file: tp.Any
    uuid: UUID
