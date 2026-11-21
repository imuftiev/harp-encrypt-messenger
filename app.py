from fastapi import FastAPI
from api.routers.user import router as user_router
from api.routers.auth import router as auth_router
from core.exception.exception_handler import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI()
    register_error_handlers(app)
    routers = [auth_router, user_router]
    for router in routers:
        app.include_router(router)
    return app


app = create_app()
