import typing as tp
from librarius.domain.models import Series
from librarius.adapters.repositories.abstract import AbstractRepository


class SeriesRepository(AbstractRepository):
    name: tp.ClassVar[str] = "series"

    def add(self, series: "Series") -> None:
        self.context.add(series)
        self.touched.add(series)

    def remove(self, series: "Series") -> None:
        self.context.remove(series)

    def find(self):
        pass
        #return self.context.query(query_object)

    def find_by_uuid(self, uuid: str) -> tp.Optional['Series']:
        return self.context.session.query(Series).filter_by(uuid=uuid).first()
