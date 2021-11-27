import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateRole(AbstractCommand["CreateRole"]):
    name: str
    role_uuid: str
    resource_names: list[str]
