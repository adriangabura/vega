import typing as tp
from datetime import datetime, date
from librarius.domain.models import Entity, date_factory
from librarius.domain.messages import events

if tp.TYPE_CHECKING:
    from librarius.domain.models.author import Author


class Publication(Entity):
    _repr_attributes = ['uuid', 'date_added', 'date_modified', 'date_published', 'title', 'authors']

    def __init__(
            self,
            uuid: str = None,
            date_added: datetime = None,
            date_modified: datetime = None,
            date_published: date = None,
            title: str = None
    ) -> None:
        super().__init__(uuid=uuid, date_added=date_added, date_modified=date_modified)
        self.date_published: date = date_factory(date_published)
        self.title: str = title
        self.authors: list["Author"] = []

    def add_publication(self) -> None:
        self.events.append(events.PublicationAdded())

    def add_author(self, author: 'Author'):
        self.authors.append(author)
        self.events.append(events.AuthorAdded())
