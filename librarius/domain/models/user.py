import typing as tp
from datetime import datetime

from librarius.domain.models import Entity


if tp.TYPE_CHECKING:
    from librarius.domain.models.publication import Publication
    from librarius.domain.models.role import Role


class User(Entity):
    _repr_attributes = ["uuid", "date_added", "date_modified", "name"]
    roles: list["Role"]

    def __init__(
        self,
        uuid: str = None,
        date_added: datetime = None,
        date_modified: datetime = None,
        name: str = None,
    ) -> None:
        super().__init__(uuid=uuid, date_added=date_added, date_modified=date_modified)
        self.name: str = name
        self.roles: list["Role"] = []
