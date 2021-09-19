import dataclasses
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateSeries(AbstractCommand['CreateSeries']):
    series_uuid: str
    name: str


@dataclasses.dataclass
class AddSeries(AbstractCommand['AddSeries']):
    pass


@dataclasses.dataclass
class ModifySeries(AbstractCommand['ModifySeries']):
    pass


@dataclasses.dataclass
class RemoveSeries(AbstractCommand['RemoveSeries']):
    pass
