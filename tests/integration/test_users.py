import typing as tp
import pytest
from librarius.adapters import repositories
from librarius.domain import models
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext

if tp.TYPE_CHECKING:
    from starlette.testclient import TestClient
    from sqlalchemy.orm import Session

pytestmark = pytest.mark.usefixtures("mappers")


def test_create_super_user(sqlite_session_factory, fastapi_test_client: "TestClient"):
    session: "Session" = sqlite_session_factory()
    context = SQLAlchemyRepositoryContext(session)
    repo = repositories.UsersRepository(context)

    u1 = models.User(name="superuser")
    repo.add(u1)
    repo.context.session.commit()

    fastapi_test_client.put("/roles/users_admin", data={"user": "superuser"}, auth=('root', 'default_password'))
    fastapi_test_client.put("/roles/groups_admin", data={"user": "superuser"}, auth=('root', 'default_password'))
    fastapi_test_client.put("/roles/policies_admin", data={"user": "superuser"}, auth=('root', 'default_password'))
    fastapi_test_client.put("/roles/roles_admin", data={"user": "superuser"}, auth=('root', 'default_password'))


    # p1 = models.Publication(title="Something")
    # p2 = models.Publication(title="Else")
    # repo.add(p1)
    # repo.add(p2)
    # session.commit()
    # [*results] = session.execute("SELECT * FROM publications")
    # print(results)
    # assert repo.find(str(p1.uuid)) == p1
    # assert repo.find(str(p2.uuid)) == p2
    # repo.remove(str(p1.uuid))
    # repo.remove(str(p2.uuid))
    # assert not repo.find(str(p1.uuid))
    # assert not repo.find(str(p2.uuid))
