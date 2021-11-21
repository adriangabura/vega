import casbin
from casbin.model import Model
from casbin import util
import pathlib

__CASBIN_MODEL__ = pathlib.Path(__file__).parent / "test.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent / "test.csv"

e = casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())
e.add_named_domain_matching_func("g", util.key_match2)

sm = e.enforce("user2", "/users/54", "GET", "domainh")
print(sm)
#e.delete_role("policies_admin")
#e.remove_policy("policies_admin", "/policies/*", "*")
#e.add_role_for_user("root", "policies_admin")


e.save_policy()
