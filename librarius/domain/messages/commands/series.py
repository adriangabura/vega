import dataclasses
from librarius.domain.messages import AbstractCommand


@dataclasses.dataclass
class CreateSeries(AbstractCommand['CreateSeries']):
    series_uuid: str
    series_name: str


@dataclasses.dataclass
class AddPublicationToSeries(AbstractCommand['AddPublicationToSeries']):
    series_uuid: str
    series_name: str
    publication_uuid: str


@dataclasses.dataclass
class AddSeries(AbstractCommand['AddSeries']):
    pass


@dataclasses.dataclass
class ModifySeries(AbstractCommand['ModifySeries']):
    pass


@dataclasses.dataclass
class RemoveSeries(AbstractCommand['RemoveSeries']):
    pass
