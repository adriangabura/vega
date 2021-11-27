import uvicorn
import casbin
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi_authz import CasbinMiddleware
from librarius.entrypoints.fastapi_app import create_fastapi, start_app
from librarius.entrypoints.app_enforcer import get_enforcer
from librarius.entrypoints.authorization import BasicAuth


app = start_app(
    create_fastapi(middlewares=[
        {
            "middleware_class": CasbinMiddleware,
            "enforcer": get_enforcer()
        },
        {
            "middleware_class": AuthenticationMiddleware,
            "backend": BasicAuth()
        }
    ])
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
