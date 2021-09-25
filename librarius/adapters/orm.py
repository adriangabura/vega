import logging
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    event,
    DateTime,
    and_
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship, join, QueryContext

from librarius.domain import models

logger = logging.getLogger(__name__)

metadata = MetaData()

authors: Table = Table(
    "authors",
    metadata,
    Column("uuid", String(255), primary_key=True, autoincrement=False),
    Column("date_added", DateTime),
    Column("date_modified", DateTime),
    Column("name", String(255))
)

series: Table = Table(
    "series",
    metadata,
    Column("uuid", String(255), primary_key=True, autoincrement=False),
    Column("date_added", DateTime),
    Column("date_modified", DateTime),
    Column("name", String(255))
)

publications: Table = Table(
    "publications",
    metadata,
    Column("uuid", String(255), primary_key=True, autoincrement=False),
    Column("title", String(255)),
    Column("date_added", DateTime),
    Column("date_modified", DateTime),
    Column("date_published", Date)
)

series_publications: Table = Table(
    "series_publications",
    metadata,
    Column("series_uuid", String(255), ForeignKey('series.uuid')),
    Column("publication_uuid", String(255), ForeignKey('publications.uuid'))
)

publications_authors: Table = Table(
    "publications_authors",
    metadata,
    Column("publication_uuid", String(255), ForeignKey('publications.uuid')),
    Column("author_uuid", String(255), ForeignKey('authors.uuid'))
)


def start_mappers():
    logger.info("Starting mappers")
    mapper_registry = registry()

    # Authors
    authors_mapper = mapper_registry.map_imperatively(
        models.Author,
        authors,
        properties={
            "publications": relationship("Publication", secondary=publications_authors, back_populates="authors", lazy="joined")
        }
    )

    # Publications
    publications_mapper = mapper_registry.map_imperatively(
        models.Publication,
        publications,
        properties={
            "authors": relationship("Author", secondary=publications_authors, back_populates="publications", lazy="subquery")
        }
    )

    # Series
    series_mapper = mapper_registry.map_imperatively(
        models.Series,
        series,
        properties={
            "publications": relationship("Publication", secondary=series_publications),
            "authors": relationship(
                "Author",
                secondary=join(series_publications, publications_authors,
                               series_publications.columns.publication_uuid == publications_authors.columns.publication_uuid),
                primaryjoin=and_(series.columns.uuid == series_publications.columns.series_uuid,
                                 authors.columns.uuid == publications_authors.columns.author_uuid),
                viewonly=True,
                lazy="subquery"
            )
        })


@event.listens_for(models.Author, 'load')
def load_author(target: models.Author, context: QueryContext):
    target.events = []


@event.listens_for(models.Series, 'load')
def load_series(target: models.Series, context: QueryContext):
    target.events = []
    target.publications


@event.listens_for(models.Publication, 'load')
def load_publication(target: models.Publication, context: QueryContext):
    target.events = []

