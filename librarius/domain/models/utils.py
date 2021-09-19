import typing as tp
from uuid import uuid4, UUID
from datetime import datetime, date
# import dataclasses


# def datetime_field() -> dataclasses.Field:
#     return dataclasses.field(default_factory=datetime.now)
#
#
# def list_field() -> dataclasses.Field:
#     return dataclasses.field(default_factory=list)
#
#
# def uuid_field() -> dataclasses.Field:
#     return dataclasses.field(default_factory=uuid4)
#
#
# def stringified_uuid_field() -> dataclasses.Field:
#     def stringify_uuid_factory():
#         return str(uuid4())
#     return dataclasses.field(default_factory=stringify_uuid_factory)


def uuid_factory(value: UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    else:
        return uuid4()


def datetime_factory(value: tp.Optional[datetime]) -> datetime:
    if isinstance(value, datetime):
        return value
    else:
        return datetime.now()


def date_factory(value: tp.Optional[date]) -> date:
    if isinstance(value, date):
        return value
    else:
        return date.today()
