import pathlib

import pytest
import casbin


__CASBIN_MODEL__ = pathlib.Path(__file__).parent.parent.parent / "librarius" / "config" / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent.parent.parent / "librarius" / "config" / "rbac_policy.csv"


@pytest.fixture
def casbin_enforcer():
    return casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())
