import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from librarius.entrypoints.app_enforcer import get_enforcer

router = APIRouter(tags=["policies"])


@router.put("/policies/{policy_name}", status_code=HTTPStatus.NO_CONTENT)
def put_policy(policy_name: str, resource: str = Form(...), action: str = Form(...)):
    """Put a policy"""
    enforcer = get_enforcer()
    result = enforcer.add_policy(policy_name, resource, action)
    if result:
        enforcer.save_policy()
        return


@router.delete("/policies/{policy_name}", status_code=HTTPStatus.NO_CONTENT)
def delete_policy(policy_name: str, resource: str = Form(...), action: str = Form(...)):
    """Delete a policy"""
    enforcer = get_enforcer()
    print(policy_name, resource, action)
    result = enforcer.remove_policy(policy_name, resource, action)
    if result:
        enforcer.save_policy()
        return
