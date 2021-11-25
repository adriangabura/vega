import dataclasses
from uuid import UUID
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateResource(AbstractCommand["CreateResource"]):
    name: str
    resource_uuid: str
