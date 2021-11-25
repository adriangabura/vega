import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap
from librarius.domain.messages import commands, queries

router = APIRouter(tags=["resources"])

bus = bootstrap(start_orm=False)


@router.post("/resources/", status_code=HTTPStatus.NO_CONTENT)
def post_resource(
        username: str = Form(...),
        password: str = Form(...),
        resource_name: str = Form(...),
        resource_uuid: str = Form(...)
):
    print(username, password, resource_name, resource_uuid)
    # ce = get_enforcer()
    # if ce.enforce(username, "/resources", "POST", "domain"):
    #     bus.handle(commands.CreateResource(name=resource_name, resource_uuid=resource_uuid))
    #     resource = bus.handle(queries.ResourceByName(resource_name=resource_name))
    #     import pdb; pdb.set_trace()
