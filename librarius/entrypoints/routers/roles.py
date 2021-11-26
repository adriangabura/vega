import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap

router = APIRouter(tags=["roles"])

buss = bootstrap(start_orm=True)


def get_bus():
    return bootstrap(start_orm=False)


@router.put("/roles/{role_name}", status_code=HTTPStatus.NO_CONTENT)
def put_role_for_user(role_name: str, user: str = Form(...)):
    """Assign a role to a user"""
    enforcer = get_enforcer()
    result = enforcer.add_role_for_user(user, role_name)
    if result:
        enforcer.save_policy()
        return