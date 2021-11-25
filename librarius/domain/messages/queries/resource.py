import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class ResourceByName(AbstractQuery["ResourceByName"]):
    resource_name: str
