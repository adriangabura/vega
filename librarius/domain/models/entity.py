import typing as tp
from datetime import datetime
from uuid import UUID

from librarius.domain.models import uuid_factory, datetime_factory

if tp.TYPE_CHECKING:
    from librarius.domain.events import AbstractEvent


class Entity:
    _repr_attributes: list[str] = ['uuid', 'date_added', 'date_modified']

    @classmethod
    def _add_repr_attribute(cls, attribute: str) -> tp.NoReturn:
        if attribute in cls.__class__ and attribute not in cls._repr_attributes:
            cls._repr_attributes.append(attribute)
        else:
            raise KeyError

    def _get_repr_attribute(self, attribute: str) -> tp.Union[str, bool]:
        value = self.__dict__.get(attribute)
        return f"{attribute}={value}" if value is not None else None

    def __init__(
            self,
            uuid: str = None,
            date_added: datetime = None,
            date_modified: datetime = None
    ) -> None:
        self.uuid: str = str(uuid_factory(uuid))
        self.date_added: datetime = datetime_factory(date_added)
        self.date_modified: datetime = datetime_factory(date_modified)
        self.events: list["AbstractEvent"] = []

    def __repr__(self) -> str:
        attributes = [self._get_repr_attribute(attribute) for attribute in self._repr_attributes if self._get_repr_attribute(attribute) is not None]
        return f"{self.__class__.__name__}({', '.join(attributes)})"
