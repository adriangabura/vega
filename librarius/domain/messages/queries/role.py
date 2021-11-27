import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class RoleByName(AbstractQuery["RoleByName"]):
    role_name: str
