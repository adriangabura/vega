import typing as tp
import uuid
from decimal import Decimal
from http import HTTPStatus
from pydantic import BaseModel


from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, Request
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.bootstrap import bootstrap
from librarius.domain.messages import commands, queries

if tp.TYPE_CHECKING:
    from librarius.domain import models

router = APIRouter(tags=["resources"])


def get_bus():
    return bootstrap(start_orm=False)


@router.post("/resources/", status_code=HTTPStatus.NO_CONTENT)
def post_resource(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        resource_name: str = Form(...),
        resource_uuid: str = Form(...),
        bus=Depends(get_bus)
):

    ce = get_enforcer()
    if ce.enforce(username, request.url.path, request.method):
        bus.handle(commands.CreateResource(name=resource_name, resource_uuid=resource_uuid))
        resource: "models.Resource" = bus.handle(queries.ResourceByName(resource_name=resource_name))
        return {"resource_name": resource.name, "resource_uuid": resource.uuid}
