import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class UserByUsername(AbstractQuery["UserByUsername"]):
    username: str
