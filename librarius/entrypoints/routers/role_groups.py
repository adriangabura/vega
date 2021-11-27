import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, Request, Body
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap
from librarius.domain.messages import commands, queries

if tp.TYPE_CHECKING:
    from librarius.domain import models

router = APIRouter(tags=["role_groups"])

# bootstrap(start_orm=True)


def get_bus():
    return bootstrap(start_orm=False)


@router.get("/role_groups/{role_group_name}", status_code=HTTPStatus.OK)
def get_role_group_by_name(role_group_name: str, bus=Depends(get_bus)):
    role_group: "models.RoleGroup" = bus.handle(queries.RoleGroupByName(role_group_name=role_group_name))
    return {
        "role_group_name": role_group.name,
        "role_group_uuid": role_group.uuid,
        "roles": [role.name for role in role_group.roles]
    }


@router.post("/role_groups/", status_code=HTTPStatus.CREATED)
def post_role_group(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        role_group_name: str = Form(...),
        role_group_uuid: str = Form(...),
        roles: list = Body(...),
        bus=Depends(get_bus)
):
    ce = get_enforcer()
    if ce.enforce(username, request.url.path, request.method):
        bus.handle(commands.CreateRoleGroup(name=role_group_name, role_group_uuid=role_group_uuid, role_names=roles))
        role_group: "models.RoleGroup" = bus.handle(queries.RoleGroupByName(role_group_name=role_group_name))
        return {
            "role_group_name": role_group.name,
            "role_group_uuid": role_group.uuid,
            "roles": [role.name for role in role_group.roles]
        }


@router.put("/roles/{role_name}", status_code=HTTPStatus.NO_CONTENT)
def put_role_for_user(role_name: str, user: str = Form(...)):
    """Assign a role to a user"""
    enforcer = get_enforcer()
    result = enforcer.add_role_for_user(user, role_name)
    if result:
        enforcer.save_policy()
        return


@router.delete("/roles/{role_name}", status_code=HTTPStatus.NO_CONTENT)
def delete_role(role_name: str, ):
    """Delete a role entirely along with the policies."""
    enforcer = get_enforcer()
    result = enforcer.delete_role(role_name)
    if result:
        enforcer.save_policy()
        return
