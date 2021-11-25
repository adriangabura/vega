import pathlib

import pytest
import casbin
from casbin import util


__CASBIN_MODEL__ = pathlib.Path(__file__).parent.parent.parent / "librarius" / "config" / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent.parent.parent / "librarius" / "config" / "rbac_policy.csv"


@pytest.fixture
def casbin_policy_blank() -> None:
    """Sets a clean policy file on which we build fixtures."""
    if __CASBIN_POLICY__.exists():
        with open(__CASBIN_POLICY__, 'w') as file:
            file.write("p, root, /*, *, *")
    else:
        with open(__CASBIN_POLICY__, 'x') as file:
            file.write("p, root, /*, *, *")
    yield
    if __CASBIN_POLICY__.exists():
        with open(__CASBIN_POLICY__, 'w') as file:
            file.write("p, root, /*, *, *")


@pytest.fixture
def casbin_enforcer() -> casbin.Enforcer:
    """Returns a Casbin Enforcer"""
    enf = casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())
    enf.add_named_domain_matching_func("g", util.key_match2_func)
    return enf


@pytest.fixture
def supergroup_role(casbin_enforcer: casbin.Enforcer) -> None:
    """Creates dynamically a superuser role."""
    ce = casbin_enforcer
    ce.add_policy("*", "/login", "*", "*")
    ce.add_policy("superadmin_users_role", "/users/{id}", "*", "*")
    ce.add_policy("superadmin_all_users_role", "/users/", "*", "*")
    ce.add_policy("superadmin_groups_role", "/groups/{id}", "*", "*")
    ce.add_policy("superadmin_all_groups_role", "/groups/", "*", "*")
    ce.add_policy("superadmin_policies_role", "/policies/{id}", "*", "*")
    ce.add_policy("superadmin_all_policies_role", "/policies/", "*", "*")
    ce.add_policy("superadmin_roles_role", "/roles/{id}", "*", "*")
    ce.add_policy("superadmin_all_roles_role", "/roles/", "*", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_users_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_all_users_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_groups_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_all_groups_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_policies_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_all_policies_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_roles_role", "*")
    ce.add_grouping_policy("supergroup_role", "superadmin_all_roles_role", "*")
    ce.add_role_for_user_in_domain("superadmin", "supergroup_role", "*")
    ce.save_policy()
