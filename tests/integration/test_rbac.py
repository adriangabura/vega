import typing as tp
import uuid

import pytest
from librarius.adapters import repositories
from librarius.domain import models
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext

if tp.TYPE_CHECKING:
    from starlette.testclient import TestClient
    from sqlalchemy.orm import Session

pytestmark = pytest.mark.usefixtures("casbin_policy_blank")


def _resource_payload() -> dict:
    return {
        "username": "root",
        "password": "default_password",
        "resource_name": "/users/321",
        "resource_uuid": str(uuid.uuid4())
    }


def test_create_resource(
        fastapi_start_app,
        fastapi_test_client: "TestClient",
        sqlite_bus
):
    fatc = fastapi_test_client
    from librarius.entrypoints.routers.resources import get_bus
    fastapi_start_app.dependency_overrides[get_bus] = lambda: sqlite_bus
    data = _resource_payload()

    response = fatc.post("/resources/", data=data, auth=('root', 'default_password'))
    jsonified = response.json()
    assert jsonified["resource_name"] == data["resource_name"]
    assert jsonified["resource_uuid"] == data["resource_uuid"]



# def test_create_super_user(sqlite_session_factory, fastapi_test_client: "TestClient"):
#     session: "Session" = sqlite_session_factory()
#     context = SQLAlchemyRepositoryContext(session)
#     repo = repositories.UsersRepository(context)
#
#     u1 = models.User(name="superuser")
#     repo.add(u1)
#     repo.context.session.commit()
#
#     fastapi_test_client.put("/roles/supergroup_role", data={"user": "superuser"}, auth=('root', 'default_password'))



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
