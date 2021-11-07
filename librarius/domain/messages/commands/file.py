import typing as tp
import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class StoreFile(AbstractCommand["StoreFile"]):
    file: tp.Any
    uuid: UUID
