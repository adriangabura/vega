import typing as tp
import abc
from uuid import uuid4, UUID
from dataclasses import dataclass, field

TAbstractMessage = tp.TypeVar('TAbstractMessage', bound="AbstractMessage")


def uuid4_factory():
    return str(uuid4())


@dataclass
class AbstractMessage(abc.ABC, tp.Generic[TAbstractMessage]):
    uuid: str = field(default_factory=uuid4_factory, init=False)


TAbstractCommand = tp.TypeVar('TAbstractCommand', bound='AbstractCommand')


@dataclass
class AbstractCommand(AbstractMessage[TAbstractCommand],tp.Generic[TAbstractCommand]):
    pass


TAbstractEvent = tp.TypeVar('TAbstractEvent', bound='AbstractEvent')


@dataclass
class AbstractEvent(AbstractMessage[TAbstractEvent], tp.Generic[TAbstractEvent]):
    pass


TAbstractQuery = tp.TypeVar('TAbstractQuery', bound='AbstractQuery')


@dataclass
class AbstractQuery(AbstractMessage[TAbstractQuery], tp.Generic[TAbstractQuery]):
    pass
