import dataclasses
from librarius.domain.messages import AbstractQuery


@dataclasses.dataclass
class AllSeries(AbstractQuery['AllSeries']):
    pass


@dataclasses.dataclass
class SeriesByUuid(AbstractQuery['SeriesByUuid']):
    series_uuid: str
