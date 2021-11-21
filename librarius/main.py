import pathlib
import uvicorn
import casbin
from fastapi_authz import CasbinMiddleware
from librarius.entrypoints.fastapi_app import create_fastapi, start_app

__CASBIN_MODEL__ = pathlib.Path(__file__).parent / "config" / "rbac_model.conf"
__CASBIN_POLICY__ = pathlib.Path(__file__).parent / "config" / "rbac_policy.csv"

app = start_app(
    create_fastapi(middlewares=[
        {
            "middleware_class": CasbinMiddleware,
            "enforcer": casbin.Enforcer(__CASBIN_MODEL__.__str__(), __CASBIN_POLICY__.__str__())
        }
    ])
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)