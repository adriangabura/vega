import typing as tp
import abc

TAbstractMessage = tp.TypeVar('TAbstractMessage', bound="AbstractMessage")


class AbstractMessage(abc.ABC, tp.Generic[TAbstractMessage]):
    pass


TAbstractCommand = tp.TypeVar('TAbstractCommand', bound='AbstractCommand')


class AbstractCommand(AbstractMessage[TAbstractCommand],tp.Generic[TAbstractCommand]):
    pass


TAbstractEvent = tp.TypeVar('TAbstractEvent', bound='AbstractEvent')


class AbstractEvent(AbstractMessage[TAbstractEvent], tp.Generic[TAbstractEvent]):
    pass


TAbstractQuery = tp.TypeVar('TAbstractQuery', bound='AbstractQuery')


class AbstractQuery(AbstractMessage[TAbstractQuery], tp.Generic[TAbstractQuery]):
    pass
