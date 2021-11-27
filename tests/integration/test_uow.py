import typing as tp
from datetime import datetime, date
from uuid import uuid4
import pytest
from sqlalchemy import text

from librarius.domain.models import Publication
from librarius.service.uow.implementation import GenericUnitOfWork

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sqlalchemy.sql.expression import TextClause
    from librarius.types import Reference

pytestmark = pytest.mark.usefixtures("mappers")


def insert_publications(
    session: "Session",
    uuid: "Reference",
    title: str,
    date_added: datetime,
    date_modified: datetime,
    date_published: date,
):
    expression: "TextClause" = text(
        "INSERT INTO publications (uuid, title, date_added, date_modified, date_published) VALUES (:uuid, :title, :date_added, :date_modified, :date_published)"
    )
    expression: "TextClause" = expression.bindparams(
        uuid=uuid,
        title=title,
        date_added=date_added,
        date_modified=date_modified,
        date_published=date_published,
    )
    session.execute(expression)


def retrieve(query, uow):
    with uow:
        return uow.session.query(Publication).all()


def test_uow_can_retrieve_a_publication(sqlite_session_factory):
    session: "Session" = sqlite_session_factory()
    pub_uuid = str(uuid4())
    insert_publications(
        session, pub_uuid, "Cerbulan Book", datetime.now(), datetime.now(), date.today()
    )
    session.commit()

    uow = GenericUnitOfWork(sqlite_session_factory)

    # with uow:
    # results = uow.session.query(Publication).all()


#     results = retrieve_all_publications(AllPublications(), uow)
#    print(results[0].__dict__)


# def test_1(sqlite_session_factory):
#    session: Session = sqlite_session_factory()
#    uu = str(uuid.uuid4())
#    title = "Cerbulan"
#    date_added = datetime.now()
#    date_modified = datetime.now()
#    date_published = datetime.now()
#    #session.execute("INSERT INTO publications (uuid, title, date_added, date_modified, date_published VALUES (:uuid, :title, :date_added, :date_modified, :date_published)),",
#    #                dict(uuid=uu, title=title, date_added=date_added, date_modified=date_modified, date_published=date_published))
#    #insert_publications(session, uu, title, date_added, date_modified, date_published)
#    expression: TextClause = text(
#        "INSERT INTO publications (uuid, title, date_added, date_modified, date_published) VALUES (:uuid, :title, :date_added, :date_modified, :date_published)"
#    )
#    expression: TextClause = expression.bindparams(
#        uuid=uu, title=title, date_added=date_added, date_modified=date_modified, date_published=date_published
#    )
#    session.execute(expression)
#     from sqlalchemy.engine.cursor import CursorResult
#     session.commit()
#     result: CursorResult = session.execute("SELECT * FROM publications")
#     [berba] = result
#     #print(berba)
#     p1: Publication = session.query(Publication).filter_by(uuid=uu).first()
#     assert p1.uuid == uu
#
