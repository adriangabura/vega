import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class RoleGroupByName(AbstractQuery["RoleGroupByName"]):
    role_group_name: str
