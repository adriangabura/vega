import typing as tp
from librarius.adapters.repositories.abstract import AbstractRepository

if tp.TYPE_CHECKING:
    from librarius.types import Reference
    from librarius.domain.models import Publication


class PublicationsRepository(AbstractRepository):
    name: tp.ClassVar[str] = "publications"

    def add(self, publication: "Publication") -> None:
        self.context.add(publication)
        self.seen.add(publication)

    def remove(self, publication: "Publication") -> None:
        self.context.remove(publication)

    def find(self):
        pass
        #return self.context.query(query_object)
