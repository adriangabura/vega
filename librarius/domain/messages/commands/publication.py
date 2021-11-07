import typing as tp
import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreatePublication(AbstractCommand["CreatePublication"]):
    publication_uuid: str
    title: str


@dataclasses.dataclass
class AddAuthorToPublication(AbstractCommand["AddAuthorToPublication"]):
    publication_uuid: str
    author_uuid: str
    author_name: str


@dataclasses.dataclass
class ModifyPublication(AbstractCommand["ModifyPublication"]):
    pass


@dataclasses.dataclass
class RemovePublication(AbstractCommand["RemovePublication"]):
    pass
