import typing as tp
import uuid

import pytest
from librarius.adapters import repositories
from librarius.domain import models
from librarius.adapters.repositories.contexts import SQLAlchemyRepositoryContext

if tp.TYPE_CHECKING:
    from starlette.testclient import TestClient
    from sqlalchemy.orm import Session

pytestmark = pytest.mark.usefixtures("casbin_policy_blank", "mappers", "supergroup_role")


def _resource_payload() -> dict:
    return {
        "username": "root",
        "password": "default_password",
        "resource_name": "/users/321",
        "resource_uuid": str(uuid.uuid4())
    }


def _role_payload():
    return {
        "username": "root",
        "password": "default_password",
        "role_name": "driver",
        "role_uuid": str(uuid.uuid4())
    }


def _role_group_payload():
    return {
        "username": "root",
        "password": "default_password",
        "role_group_name": "superadm",
        "role_group_uuid": str(uuid.uuid4())
    }


def _user_payload():
    return {
        "username": "root",
        "password": "default_password",
        "user_username": "cerbulan",
        "user_uuid": str(uuid.uuid4())
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


def test_create_role(
        fastapi_start_app,
        fastapi_test_client: "TestClient",
        sqlite_bus
):
    fatc = fastapi_test_client
    from librarius.entrypoints.routers.roles import get_bus
    fastapi_start_app.dependency_overrides[get_bus] = lambda: sqlite_bus
    data = _role_payload()
    data["resources"] = ["/users/321"]

    response = fatc.post("/roles/", data=data, auth=('root', 'default_password'))
    jsonified = response.json()
    assert jsonified["role_name"] == data["role_name"]
    assert jsonified["role_uuid"] == data["role_uuid"]


def test_create_user(
        fastapi_start_app,
        fastapi_test_client: "TestClient",
        sqlite_bus
):
    fatc = fastapi_test_client
    from librarius.entrypoints.routers.users import get_bus
    fastapi_start_app.dependency_overrides[get_bus] = lambda: sqlite_bus
    data = _user_payload()
    data["roles"] = ["driver"]

    response = fatc.post("/users/", data=data, auth=('root', 'default_password'))
    jsonified = response.json()
    assert jsonified["user_username"] == data["user_username"]
    assert jsonified["user_uuid"] == data["user_uuid"]

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
