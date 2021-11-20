import casbin
from fastapi import FastAPI
from fastapi_authz import CasbinMiddleware

from librarius.entrypoints.routers import users_router


def create_fastapi(**kwargs) -> FastAPI:
    options: dict = kwargs.setdefault("options", dict())
    app: FastAPI = kwargs.setdefault("app", FastAPI(**options))
    middlewares: list = kwargs.setdefault("middlewares", list())

    for middleware in middlewares:
        app.add_middleware(**middleware)

    return FastAPI()


_app = create_fastapi(middlewares=[
    {
        "middleware_class": CasbinMiddleware,
        "enforcer": casbin.Enforcer()
    }
])


def start_app(app: FastAPI = _app):
    app.include_router(users_router)

    @app.get("/")
    async def read_main():
        return {"msg": "Hello World"}

    return app
