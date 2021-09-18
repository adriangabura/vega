import typing as tp
import pytest
from librarius.adapters import repositories
from librarius.domain import models
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext

if tp.TYPE_CHECKING:
    from sqlalchemy.orm import Session

pytestmark = pytest.mark.usefixtures("mappers")


def test_add_find_and_remove_publications(sqlite_session_factory):
    session: "Session" = sqlite_session_factory()
    context = SQLAlchemyRepositoryContext(session)
    repo = repositories.PublicationsRepository(context)
    p1 = models.Publication(title="Something")
    p2 = models.Publication(title="Else")
    repo.add(p1)
    repo.add(p2)
    session.commit()
    [*results] = session.execute("SELECT * FROM publications")
    print(results)
    #assert repo.find(str(p1.uuid)) == p1
    #assert repo.find(str(p2.uuid)) == p2
    #repo.remove(str(p1.uuid))
    #repo.remove(str(p2.uuid))
    #assert not repo.find(str(p1.uuid))
    #assert not repo.find(str(p2.uuid))
