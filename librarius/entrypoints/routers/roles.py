import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap

router = APIRouter(tags=["roles"])

bus = bootstrap()

@router.get("roles/")
def gets():
    return 423423


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
