import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateAuthor(AbstractCommand["CreateAuthor"]):
    name: str
    author_uuid: str


@dataclasses.dataclass
class AuthorBaseCommand(AbstractCommand["AuthorBaseCommand"]):
    pass


@dataclasses.dataclass
class AddAuthor(AuthorBaseCommand):
    name: str


@dataclasses.dataclass
class ModifyAuthor(AuthorBaseCommand):
    pass


@dataclasses.dataclass
class RemoveAuthor(AuthorBaseCommand):
    pass
