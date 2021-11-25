import typing as tp
from librarius.domain.models import User
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext


class UsersRepository(
    AbstractRepository["UsersRepository", SQLAlchemyRepositoryContext]
):
    name: tp.ClassVar[str] = "users"

    def add(self, user: "User") -> None:
        self.context.add(user)
        # AuthorCreated Event
        self.touched.add(user)

    def remove(self, user: "User") -> None:
        self.context.remove(user)
        self.touched.add(user)

    def find(self):
        pass
        # return self.context.query(query_object)

    def find_by_uuid(self, uuid) -> tp.Optional["User"]:
        return self.context.session.query(User).filter_by(uuid=uuid).first()
