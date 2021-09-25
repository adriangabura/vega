import typing as tp
from datetime import datetime
from librarius.domain.models import Entity
from librarius.domain.messages import events

if tp.TYPE_CHECKING:
    from librarius.domain.models.author import Author, Publication


class Series(Entity):
    _repr_attributes = ['uuid', 'date_added', 'date_modified', 'name', 'publications', 'authors']
    publications: list["Publication"]
    authors: list["Author"]

    def __init__(
            self,
            uuid: str = None,
            date_added: datetime = None,
            date_modified: datetime = None,
            name: str = None
    ) -> None:
        super().__init__(uuid=uuid, date_added=date_added, date_modified=date_modified)
        self.name: str = name
        self.publications: list["Publication"] = []
        self.authors: list["Author"] = []

    def add_publication(self, publication: 'Publication'):
        self.publications.append(publication)
        self.events.append(events.PublicationAddedToSeries())
