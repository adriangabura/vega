import typing as tp
import pytest

from starlette.middleware.authentication import AuthenticationMiddleware

from fastapi.testclient import TestClient
from fastapi_authz import CasbinMiddleware

from librarius.entrypoints.fastapi_app import create_fastapi, start_app

if tp.TYPE_CHECKING:
    from fastapi import FastAPI


@pytest.fixture
def fastapi_create_app(casbin_enforcer, basic_auth) -> "FastAPI":
    yield create_fastapi(
        middlewares=[
            {
                "middleware_class": CasbinMiddleware,
                "enforcer": casbin_enforcer
            },
            {
                "middleware_class": AuthenticationMiddleware,
                "backend": basic_auth()
            }
        ]
    )


@pytest.fixture
def fastapi_start_app(fastapi_create_app) -> "FastAPI":
    return start_app(fastapi_create_app)


@pytest.fixture
def fastapi_test_client(fastapi_start_app) -> "TestClient":
    return TestClient(fastapi_start_app)
