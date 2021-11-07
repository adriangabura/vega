import typing as tp
from librarius.domain.models import Publication
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext

if tp.TYPE_CHECKING:
    from librarius.types import Reference


class PublicationsRepository(
    AbstractRepository["PublicationsRepository", SQLAlchemyRepositoryContext]
):
    name: tp.ClassVar[str] = "publications"

    def add(self, publication: "Publication") -> None:
        self.context.add(publication)
        self.touched.add(publication)

    def remove(self, publication: "Publication") -> None:
        self.context.remove(publication)

    def find(self):
        pass
        # return self.context.query(query_object)

    def find_by_uuid(self, uuid: str) -> tp.Optional["Publication"]:
        return self.context.session.query(Publication).filter_by(uuid=uuid).first()
