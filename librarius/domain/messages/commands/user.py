import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateUser(AbstractCommand["CreateUser"]):
    name: str
    user_uuid: str
    roles: list[str]  # Just the role names
