import typing as tp
from librarius.domain.models import Author
from librarius.adapters.repositories.abstract import AbstractRepository
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext


class AuthorsRepository(
    AbstractRepository["AuthorsRepository", SQLAlchemyRepositoryContext]
):
    name: tp.ClassVar[str] = "authors"

    def add(self, author: "Author") -> None:
        self.context.add(author)
        # AuthorCreated Event
        self.touched.add(author)

    def remove(self, author: "Author") -> None:
        self.context.remove(author)
        self.touched.add(author)

    def find(self):
        pass
        # return self.context.query(query_object)

    def find_by_uuid(self, uuid) -> tp.Optional["Author"]:
        return self.context.session.query(Author).filter_by(uuid=uuid).first()
