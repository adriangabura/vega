import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateRoleGroup(AbstractCommand["CreateRoleGroup"]):
    name: str
    role_group_uuid: str
    role_names: list[str]
