import typing as tp
import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form

router = APIRouter(tags=["users"])


@router.get("/users/")
def get_users():
    return [{"a": "b"}]


@router.post("/users")
def post_users():
    return True


@router.delete("/users/{user_uuid}")
def delete_user():
    return True
