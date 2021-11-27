import typing as tp
from librarius.domain.models import Resource
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext


class ResourcesRepository(
    AbstractRepository["ResourcesRepository", SQLAlchemyRepositoryContext]
):
    name: tp.ClassVar[str] = "resources"

    def add(self, resource: "Resource") -> None:
        self.context.add(resource)
        # AuthorCreated Event
        self.touched.add(resource)

    def remove(self, resource: "Resource") -> None:
        self.context.remove(resource)
        self.touched.add(resource)

    def find(self):
        pass
        # return self.context.query(query_object)

    def find_by_uuid(self, uuid) -> tp.Optional["Resource"]:
        return self.context.session.query(Resource).filter_by(uuid=uuid).first()

    def find_by_name(self, name: str) -> tp.Optional["Resource"]:
        return self.context.session.query(Resource).filter_by(name=name).first()
