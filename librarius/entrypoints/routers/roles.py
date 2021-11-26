import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, Request, Body
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap

router = APIRouter(tags=["roles"])

# bootstrap(start_orm=True)


def get_bus():
    return bootstrap(start_orm=False)


@router.post("/roles/", status_code=HTTPStatus.NO_CONTENT)
def post_role(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        role_name: str = Form(...),
        role_uuid: str = Form(...),
        bus=Depends(get_bus)
):
    pass


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
