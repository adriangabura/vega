import typing as tp
from librarius.domain.models import Role
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext


class RolesRepository(
    AbstractRepository["RolesRepository", SQLAlchemyRepositoryContext]
):
    name: tp.ClassVar[str] = "roles"

    def add(self, role: "Role") -> None:
        self.context.add(role)
        # AuthorCreated Event
        self.touched.add(role)

    def remove(self, role: "Role") -> None:
        self.context.remove(role)
        self.touched.add(role)

    def find(self):
        pass
        # return self.context.query(query_object)

    def find_by_uuid(self, uuid) -> tp.Optional["Role"]:
        return self.context.session.query(Role).filter_by(uuid=uuid).first()

    def find_by_name(self, name: str) -> tp.Optional["Role"]:
        return self.context.session.query(Role).filter_by(name=name).first()
