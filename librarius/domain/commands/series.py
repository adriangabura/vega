import dataclasses
from librarius.domain.commands import AbstractCommand


@dataclasses.dataclass
class AddSeries(AbstractCommand):
    pass


@dataclasses.dataclass
class ModifySeries(AbstractCommand):
    pass


@dataclasses.dataclass
class RemoveSeries(AbstractCommand):
    pass
