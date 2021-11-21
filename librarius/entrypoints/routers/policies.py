import typing as tp
import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form

router = APIRouter(tags=["policies"])

from pydantic import BaseModel


class PolicyPutBody(BaseModel):
    resource: str
    action: str


@router.get("/policies/")
def get_policy():
    return [{"a": "b"}]


@router.put("/policies/{policy_name}")
def put_policy(policy_name: str, resource: str = Form(...), action: str = Form(...)):
    return [resource, action]


@router.delete("/policies/{policy_name}")
def delete_policy(policy_name: str):
    return True
