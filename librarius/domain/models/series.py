import typing as tp
import logging
from datetime import datetime
from librarius.domain.models import Entity
from librarius.domain.messages import events

if tp.TYPE_CHECKING:
    from librarius.domain.models.author import Author, Publication

logger = logging.getLogger(__name__)


class Series(Entity):
    _repr_attributes = ['uuid', 'date_added', 'date_modified', 'name', 'publications', 'authors']
    publications: set["Publication"]
    authors: set["Author"]

    def __init__(
            self,
            uuid: str = None,
            date_added: datetime = None,
            date_modified: datetime = None,
            name: str = None
    ) -> None:
        super().__init__(uuid=uuid, date_added=date_added, date_modified=date_modified)
        self.name: str = name
        self.publications: set["Publication"] = set()
        self.authors: set["Author"] = set()

    def add_publication(self, publication: 'Publication'):
        if publication not in self.publications:
            self.publications.add(publication)
            self.events.append(events.PublicationAddedToSeries())
        else:
            logger.debug('Publication already is assigned.')
