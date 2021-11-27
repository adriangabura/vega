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
            file.write("p, root, /*, *")
    else:
        with open(__CASBIN_POLICY__, 'x') as file:
            file.write("p, root, /*, *")
    yield
    if __CASBIN_POLICY__.exists():
        with open(__CASBIN_POLICY__, 'w') as file:
            file.write("p, root, /*, *")


@pytest.mark.usefixtures("casbin_policy_blank")
@pytest.fixture
def casbin_enforcer() -> casbin.Enforcer:
    """Returns a Casbin Enforcer"""
    enf = casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())
    enf.add_named_domain_matching_func("g", util.key_match2_func)
    return enf
