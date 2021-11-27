import typing as tp
import uuid

import pytest

if tp.TYPE_CHECKING:
    from starlette.testclient import TestClient


@pytest.mark.usefixtures("mappers")
@pytest.fixture
def supergroup_role(fastapi_start_app, fastapi_test_client: "TestClient", sqlite_bus):
    fatc = fastapi_test_client
    from librarius.entrypoints.routers.resources import get_bus
    fastapi_start_app.dependency_overrides[get_bus] = lambda: sqlite_bus

    superadmin_users_resource = "/users/{id}"
    superadmin_all_users_resource = "/users/"
    superadmin_groups_resource = "/groups/{id}"
    superadmin_all_groups_resource = "/groups/"
    superadmin_policies_resource = "/policies/{id}"
    superadmin_all_policies_resource = "/policies/"
    superadmin_roles_resource = "/roles/{id}"
    superadmin_all_roles_resource = "/roles/"

    resources = [
        superadmin_users_resource,
        superadmin_all_users_resource,
        superadmin_groups_resource,
        superadmin_all_groups_resource,
        superadmin_policies_resource,
        superadmin_all_policies_resource,
        superadmin_roles_resource,
        superadmin_all_roles_resource
    ]

    for resource_name in resources:
        fatc.post(
            "/resources/",
            data={
                "username": "root",
                "password": "default_password",
                "resource_name": resource_name,
                "resource_uuid": str(uuid.uuid4())
            },
            auth=('root', 'default_password'))

# @pytest.fixture
# def supergroup_role(casbin_enforcer: casbin.Enforcer) -> None:
#     """Creates dynamically a superuser role."""
#     ce = casbin_enforcer
#     ce.add_policy("*", "/login", "*", "*")
#     ce.add_policy("superadmin_users_role", "/users/{id}", "*", "*")
#     ce.add_policy("superadmin_all_users_role", "/users/", "*", "*")
#     ce.add_policy("superadmin_groups_role", "/groups/{id}", "*", "*")
#     ce.add_policy("superadmin_all_groups_role", "/groups/", "*", "*")
#     ce.add_policy("superadmin_policies_role", "/policies/{id}", "*", "*")
#     ce.add_policy("superadmin_all_policies_role", "/policies/", "*", "*")
#     ce.add_policy("superadmin_roles_role", "/roles/{id}", "*", "*")
#     ce.add_policy("superadmin_all_roles_role", "/roles/", "*", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_users_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_users_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_groups_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_groups_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_policies_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_policies_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_roles_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_roles_role", "*")
#     ce.add_role_for_user_in_domain("superadmin", "supergroup_role", "*")
#     ce.save_policy()
