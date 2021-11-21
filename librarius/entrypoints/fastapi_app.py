import casbin
from fastapi import FastAPI
from fastapi_authz import CasbinMiddleware

from librarius.entrypoints.routers import users_router, policies_router


def create_fastapi(**kwargs) -> FastAPI:
    options: dict = kwargs.setdefault("options", dict())
    app: FastAPI = kwargs.setdefault("app", FastAPI(**options))
    middlewares: list = kwargs.setdefault("middlewares", list())

    for middleware in middlewares:
        app.add_middleware(**middleware)

    return app


def start_app(app: FastAPI):
    app.include_router(users_router)
    app.include_router(policies_router)

    @app.get("/")
    async def read_main():
        return {"msg": "Hello World"}

    return app
