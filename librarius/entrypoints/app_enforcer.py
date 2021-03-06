import pathlib
import casbin
from casbin import util

__CASBIN_MODEL__ = pathlib.Path(__file__).parent.parent / "config" / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent.parent / "config" / "rbac_policy.csv"


def create_enforcer(model: pathlib.Path, policy: pathlib.Path) -> casbin.Enforcer:
    """Takes Path inputs and translates them to str to output an enforcer"""
    enforcer = casbin.Enforcer(model.__str__(), policy.__str__())
    enforcer.add_named_domain_matching_func("g", util.key_match2_func)
    return enforcer


_enforcers = [create_enforcer(__CASBIN_MODEL__, __CASBIN_POLICY__)]


def get_enforcer() -> casbin.Enforcer:
    if len(_enforcers) == 1:
        return _enforcers[0]