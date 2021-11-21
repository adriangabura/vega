import typing as tp
import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form

router = APIRouter(tags=["policy"])


@router.get("/policy/")
def get_policy():
    return [{"a": "b"}]


@router.put("/policy/{policy_name}")
def put_policy(policy_name: str):
    return True


@router.delete("/policy/{policy_name}")
def delete_policy(policy_name: str):
    return True
