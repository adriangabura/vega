import casbin
import pathlib

__CASBIN_MODEL__ = pathlib.Path(__file__).parent / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent / "rbac_policy.csv"

e = casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())

e.add_policy("superusers_admin", "/users/*", "*")
e.add_role_for_user("root3", "superusers_admin")

e.save_policy()
