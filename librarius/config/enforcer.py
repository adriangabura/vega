import casbin
from casbin.model import Model
from casbin import util
import pathlib

__CASBIN_MODEL__ = pathlib.Path(__file__).parent / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent / "rbac_policy.csv"

e = casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())
e.add_named_domain_matching_func("g", util.key_match2_func)

result = e.enforce("root", "/resources", "GET", "domain")
print(result)
#e.delete_role("policies_admin")
#e.remove_policy("policies_admin", "/policies/*", "*")
#e.add_role_for_user("root", "policies_admin")


#e.save_policy()
