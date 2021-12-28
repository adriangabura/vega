import typing as tp
from librarius.domain.models import RoleGroup
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext


class RoleGroupsRepository(
    AbstractRepository["RoleGroupsRepository", SQLAlchemyRepositoryContext]
):
    name: tp.ClassVar[str] = "role_groups"

    def add(self, role_group: "RoleGroup") -> None:
        self.context.add(role_group)
        # AuthorCreated Event
        self.touched.add(role_group)

    def remove(self, role_group: "RoleGroup") -> None:
        self.context.remove(role_group)
        self.touched.add(role_group)

    def find(self):
        pass
        # return self.context.query(query_object)

    def find_by_uuid(self, uuid) -> tp.Optional["RoleGroup"]:
        return self.context.session.query(RoleGroup).filter_by(uuid=uuid).first()

    def find_by_name(self, name: str) -> tp.Optional["RoleGroup"]:
        return self.context.session.query(RoleGroup).filter_by(name=name).first()
