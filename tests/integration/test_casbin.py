import typing as tp
from datetime import datetime, date
from uuid import uuid4

import pytest

pytestmark = pytest.mark.usefixtures("casbin_policy_blank")


@pytest.mark.usefixtures("supergroup_role")
def test_supergroup_role(casbin_enforcer):
    ce = casbin_enforcer
    assert ce.enforce("superadmin", "/wrong_endpoint/", "GET") == False
    assert ce.enforce("superadmin", "/users/", "GET")
    assert ce.enforce("superadmin", "/users/1989", "GET")
    assert ce.enforce("superadmin", "/groups/", "GET")
    assert ce.enforce("superadmin", "/groups/1989", "GET")
    assert ce.enforce("superadmin", "/policies/", "GET")
    assert ce.enforce("superadmin", "/policies/1989", "GET")
    assert ce.enforce("superadmin", "/roles/", "GET")
    assert ce.enforce("superadmin", "/roles/1989", "GET")