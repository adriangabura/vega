import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class AuthorBaseCommand(AbstractCommand['AuthorBaseCommand']):
    uuid: str


@dataclasses.dataclass
class AddAuthor(AuthorBaseCommand):
    name: str


@dataclasses.dataclass
class ModifyAuthor(AuthorBaseCommand):
    pass


@dataclasses.dataclass
class RemoveAuthor(AuthorBaseCommand):
    pass
