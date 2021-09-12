import typing as tp
from datetime import datetime, date
from uuid import uuid4

import pytest

from sqlalchemy.sql.expression import text

from librarius.domain import models

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sqlalchemy.sql.expression import TextClause

pytestmark = pytest.mark.usefixtures("mappers")


def test_mappers(sqlite_session_factory):
    author_uuid = str(uuid4())
    series_uuid = str(uuid4())
    publication_uuid = str(uuid4())

    some_datetime = datetime.now()
    some_date = date.today()

    session: "Session" = sqlite_session_factory()

    publication_exp: "TextClause" = text(
        "INSERT INTO publications (uuid, title, date_added, date_modified, date_published) VALUES (:uuid, :title, :date_added, :date_modified, :date_published)"
    )

    publication_exp: "TextClause" = publication_exp.bindparams(
        uuid=publication_uuid,
        title="Cerbulan Book",
        date_added=some_datetime,
        date_modified=some_datetime,
        date_published=some_date
    )

    author_exp: "TextClause" = text(
        "INSERT INTO authors (uuid, name, date_added, date_modified) VALUES (:uuid, :name, :date_added, :date_modified)"
    )

    author_exp: "TextClause" = author_exp.bindparams(
        uuid=author_uuid,
        name="Cerbulan Maran",
        date_added=some_datetime,
        date_modified=some_datetime
    )

    series_exp: "TextClause" = text(
        "INSERT INTO series (uuid, name, date_added, date_modified) VALUES (:uuid, :name, :date_added, :date_modified)"
    )

    series_exp: "TextClause" = series_exp.bindparams(
        uuid=series_uuid,
        name="Cerbulan Series",
        date_added=some_datetime,
        date_modified=some_datetime
    )

    series_publications_exp: "TextClause" = text(
        "INSERT INTO series_publications (series_uuid, publication_uuid) VALUES (:series_uuid, :publication_uuid)"
    )

    series_publications_exp: "TextClause" = series_publications_exp.bindparams(
        series_uuid=series_uuid,
        publication_uuid=publication_uuid
    )

    publications_authors: "TextClause" = text(
        "INSERT INTO publications_authors (author_uuid, publication_uuid) VALUES (:author_uuid, :publication_uuid)"
    )

    publications_authors: "TextClause" = publications_authors.bindparams(
        author_uuid=author_uuid,
        publication_uuid=publication_uuid
    )

    session.execute(publication_exp)
    session.execute(author_exp)
    session.execute(series_exp)
    session.execute(series_publications_exp)
    session.execute(publications_authors)

    query_author: models.Author = session.query(models.Author).filter_by(uuid=author_uuid).first()
    query_publication: models.Publication = session.query(models.Publication).filter_by(uuid=publication_uuid).first()
    query_series: models.Series = session.query(models.Series).filter_by(uuid=series_uuid).first()

    assert query_author.uuid == author_uuid
    assert query_series.uuid == series_uuid
    assert query_publication.uuid == publication_uuid

    assert query_publication.uuid in [publication.uuid for publication in query_author.publications]
    assert query_publication.uuid in [publication.uuid for publication in query_series.publications]
    assert query_author.uuid in [author.uuid for author in query_publication.authors]
    assert query_author.uuid in [author.uuid for author in query_series.authors]
