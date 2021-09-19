import dataclasses
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class AddPublication(AbstractCommand['AddPublication']):
    title: str
    uuid: str


@dataclasses.dataclass
class AddAuthorToPublication(AbstractCommand['AddAuthorToPublication']):
    publication_uuid: str
    author_uuid: str
    author_title: str


@dataclasses.dataclass
class ModifyPublication(AbstractCommand['ModifyPublication']):
    pass


@dataclasses.dataclass
class RemovePublication(AbstractCommand['RemovePublication']):
    pass
