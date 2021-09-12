import dataclasses
from uuid import UUID
from librarius.domain.commands import AbstractCommand


@dataclasses.dataclass
class AuthorBaseCommand(AbstractCommand):
    uuid: UUID


@dataclasses.dataclass
class AddAuthor(AuthorBaseCommand):
    name: str


@dataclasses.dataclass
class ModifyAuthor(AuthorBaseCommand):
    pass


@dataclasses.dataclass
class RemoveAuthor(AuthorBaseCommand):
    pass
