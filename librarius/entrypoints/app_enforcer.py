import pathlib
import casbin

__CASBIN_MODEL__ = pathlib.Path(__file__).parent.parent / "config" / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent.parent / "config" / "rbac_policy.csv"


def create_enforcer(model: pathlib.Path, policy: pathlib.Path) -> casbin.Enforcer:
    """Takes Path inputs and translates them to str to output an enforcer"""
    return casbin.Enforcer(model.__str__(), policy.__str__())
