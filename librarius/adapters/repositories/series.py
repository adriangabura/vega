import typing as tp
from librarius.adapters.repositories.abstract import AbstractRepository

if tp.TYPE_CHECKING:
    from librarius.domain.models import Series


class SeriesRepository(AbstractRepository):
    name: tp.ClassVar[str] = "series"

    def add(self, series: "Series") -> None:
        self.context.add(series)
        self.seen.add(series)

    def remove(self, series: "Series") -> None:
        self.context.remove(series)

    def find(self):
        pass
        #return self.context.query(query_object)
