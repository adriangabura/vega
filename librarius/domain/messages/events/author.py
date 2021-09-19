import dataclasses
from librarius.domain.messages import AbstractEvent


@dataclasses.dataclass
class AuthorAdded(AbstractEvent['AuthorAdded']):
    pass


@dataclasses.dataclass
class AuthorModified(AbstractEvent['AuthorModified']):
    pass


@dataclasses.dataclass
class AuthorRemoved(AbstractEvent['AuthorRemoved']):
    pass
