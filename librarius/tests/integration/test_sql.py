import typing as tp
from datetime import datetime, date
from uuid import uuid4

import pytest

from sqlalchemy.sql.expression import text
from librarius.adapters.orm import publications
from librarius.domain import models

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sqlalchemy.sql.expression import TextClause

pytestmark = pytest.mark.usefixtures("mappers")


def test_sql(sqlite_session_factory):
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
        date_published=some_date,
    )

    author_exp: "TextClause" = text(
        "INSERT INTO authors (uuid, name, date_added, date_modified) VALUES (:uuid, :name, :date_added, :date_modified)"
    )

    author_exp: "TextClause" = author_exp.bindparams(
        uuid=author_uuid,
        name="Cerbulan Maran",
        date_added=some_datetime,
        date_modified=some_datetime,
    )

    series_exp: "TextClause" = text(
        "INSERT INTO series (uuid, name, date_added, date_modified) VALUES (:uuid, :name, :date_added, :date_modified)"
    )

    series_exp: "TextClause" = series_exp.bindparams(
        uuid=series_uuid,
        name="Cerbulan Series",
        date_added=some_datetime,
        date_modified=some_datetime,
    )

    series_publications_exp: "TextClause" = text(
        "INSERT INTO series_publications (series_uuid, publication_uuid) VALUES (:series_uuid, :publication_uuid)"
    )

    series_publications_exp: "TextClause" = series_publications_exp.bindparams(
        series_uuid=series_uuid, publication_uuid=publication_uuid
    )

    publications_authors: "TextClause" = text(
        "INSERT INTO publications_authors (author_uuid, publication_uuid) VALUES (:author_uuid, :publication_uuid)"
    )

    publications_authors: "TextClause" = publications_authors.bindparams(
        author_uuid=author_uuid, publication_uuid=publication_uuid
    )

    session.execute(publication_exp)
    session.execute(author_exp)
    session.execute(series_exp)
    session.execute(series_publications_exp)
    session.execute(publications_authors)

    s = publications.select()
    result = session.execute(s)
    print(result.fetchall()[0].uuid)
