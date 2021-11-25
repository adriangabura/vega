import typing as tp
from datetime import datetime, date
from uuid import uuid4

import pytest

pytestmark = pytest.mark.usefixtures("casbin_policy_blank")


@pytest.mark.usefixtures("supergroup_role")
def test_supergroup_role(casbin_enforcer):
    ce = casbin_enforcer
    #assert ce.enforce("superadmin", "/users/2121", "GET", "domain")
