import typing as tp
import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form

router = APIRouter(tags=["policy"])


@router.get("/policy/")
def get_users():
    return [{"a": "b"}]


@router.put("/policy/{policy_name}")
def post_users():
    return True


@router.delete("/policy/{policy_name}")
def delete_user():
    return True
