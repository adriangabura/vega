


# @pytest.fixture
# def supergroup_role(casbin_enforcer: casbin.Enforcer) -> None:
#     """Creates dynamically a superuser role."""
#     ce = casbin_enforcer
#     ce.add_policy("*", "/login", "*", "*")
#     ce.add_policy("superadmin_users_role", "/users/{id}", "*", "*")
#     ce.add_policy("superadmin_all_users_role", "/users/", "*", "*")
#     ce.add_policy("superadmin_groups_role", "/groups/{id}", "*", "*")
#     ce.add_policy("superadmin_all_groups_role", "/groups/", "*", "*")
#     ce.add_policy("superadmin_policies_role", "/policies/{id}", "*", "*")
#     ce.add_policy("superadmin_all_policies_role", "/policies/", "*", "*")
#     ce.add_policy("superadmin_roles_role", "/roles/{id}", "*", "*")
#     ce.add_policy("superadmin_all_roles_role", "/roles/", "*", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_users_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_users_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_groups_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_groups_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_policies_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_policies_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_roles_role", "*")
#     ce.add_grouping_policy("supergroup_role", "superadmin_all_roles_role", "*")
#     ce.add_role_for_user_in_domain("superadmin", "supergroup_role", "*")
#     ce.save_policy()