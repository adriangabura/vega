import casbin
import pathlib

__CASBIN_MODEL__ = pathlib.Path(__file__).parent / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent / "rbac_policy.csv"

e = casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())

#e.delete_role("policies_admin")
#e.remove_policy("policies_admin", "/policies/*", "*")
#e.add_role_for_user("root", "policies_admin")


e.save_policy()
