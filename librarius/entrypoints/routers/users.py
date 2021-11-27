import typing as tp
import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, Request, Body
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap
from librarius.domain.messages import commands, queries

if tp.TYPE_CHECKING:
    from librarius.domain import models

router = APIRouter(tags=["users"])


def get_bus():
    return bootstrap(start_orm=False)


@router.post("/users/")
def post_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        user_username: str = Form(...),
        user_uuid: str = Form(...),
        roles: list = Body(...),
        role_groups: list = Body(...),
        bus=Depends(get_bus)
):
    ce = get_enforcer()
    if ce.enforce(username, request.url.path, request.method):
        bus.handle(commands.CreateUser(name=user_username, user_uuid=user_uuid, roles=roles, role_groups=role_groups))
        user: "models.User" = bus.handle(queries.UserByUsername(username=user_username))
        return {
            "user_username": user.name, "user_uuid": user.uuid, "roles": [role.name for role in user.roles],
            "role_groups": [role_group.name for role_group in user.role_groups]
        }
