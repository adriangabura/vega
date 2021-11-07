import typing as tp
from os import getenv

import attr

from librarius.config.utils import TRegions


def from_env_var(key: str, default: str = None) -> tp.Union[str, tp.NoReturn]:
    """Returns an environmental variable value or raises an Exception."""
    value = getenv(key, default)
    if value is None:
        raise IOError("No such environmental variable found!")
    return value


def validate_string(data) -> tp.Union[str, tp.NoReturn]:
    if isinstance(data, str):
        return data
    else:
        raise ValueError("Value is not a string!")


class StringPair:
    """A stringified key:value config pair."""

    def __init__(self, key: str, value: str):
        self.key = validate_string(key)
        self.value = validate_string(value)

    def __call__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}(key={self.key}, value={self.value})"

    @classmethod
    def from_dict(cls, input_dict: dict, key: str, default: str = None) -> "StringPair":
        value = input_dict.get(key, default)
        return cls(key, value)

    @classmethod
    def from_env_var(cls, key: str, default: str = None) -> "StringPair":
        return cls(key, from_env_var(key, default))

    @classmethod
    def factory_from_env_var(cls, key: str, default: str = None) -> tp.Callable:
        return lambda: cls(key, from_env_var(key, default))()


@attr.define
class BasicConfig:
    APP_ENV: str = attr.field(
        factory=StringPair.factory_from_env_var("APP_ENV", default="local")
    )
    AWS_ACCESS_KEY_ID: str = attr.field(
        factory=StringPair.factory_from_env_var("AWS_ACCESS_KEY_ID")
    )
    AWS_SECRET_ACCESS_KEY: str = attr.field(
        factory=StringPair.factory_from_env_var("AWS_SECRET_ACCESS_KEY")
    )
    AWS_REGION: TRegions = attr.field(
        factory=StringPair.factory_from_env_var("AWS_REGION")
    )
    BUCKET_NAME: str = attr.field(
        factory=StringPair.factory_from_env_var("BUCKET_NAME")
    )
    PRESIGNED_URL_EXPIRATION: int = attr.field(
        factory=lambda: from_env_var("PRESIGNED_URL_EXPIRATION"), converter=int
    )
