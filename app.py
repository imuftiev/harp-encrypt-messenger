from fastapi import FastAPI
from api.routers.user import router as user_router
from api.routers.message import router as message_router
from api.routers.auth import router as auth_router
from core.exception.exception_handler import register_exception_handler
from core.middleware.middleware import register_middleware

def create_app() -> FastAPI:
    app = FastAPI()
    register_exception_handler(app)
    register_middleware(app)
    routers = [auth_router, user_router, message_router]
    for router in routers:
        app.include_router(router)
    return app


app = create_app()
