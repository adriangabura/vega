import typing as tp
from datetime import datetime, date
from uuid import uuid4

import pytest

pytestmark = pytest.mark.usefixtures("casbin_policy_blank")


@pytest.mark.usefixtures("supergroup_role")
def test_supergroup_role(casbin_enforcer):
    ce = casbin_enforcer
    assert ce.enforce("superadmin", "/wrong_endpoint/", "GET", "domain") == False
    assert ce.enforce("superadmin", "/users/", "GET", "domain")
    assert ce.enforce("superadmin", "/users/1989", "GET", "domain")
    assert ce.enforce("superadmin", "/groups/", "GET", "domain")
    assert ce.enforce("superadmin", "/groups/1989", "GET", "domain")
    assert ce.enforce("superadmin", "/policies/", "GET", "domain")
    assert ce.enforce("superadmin", "/policies/1989", "GET", "domain")
    assert ce.enforce("superadmin", "/roles/", "GET", "domain")
    assert ce.enforce("superadmin", "/roles/1989", "GET", "domain")