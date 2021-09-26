import typing as tp
from librarius.adapters.repositories.abstract import AbstractRepository

if tp.TYPE_CHECKING:
    from librarius.domain.models import Author


class AuthorsRepository(AbstractRepository):
    name: tp.ClassVar[str] = "authors"

    def add(self, author: "Author") -> None:
        self.context.add(author)
        self.seen.add(author)

    def remove(self, author: "Author") -> None:
        self.context.remove(author)
        self.seen.add(author)

    def find(self):
        pass
        #return self.context.query(query_object)

    def find_by_uuid(self, uuid):
        pass
