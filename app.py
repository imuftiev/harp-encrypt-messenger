from fastapi import FastAPI
from controller.user import router
from core.exception.exception_handler import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI()
    register_error_handlers(app)
    app.include_router(router)
    return app


app = create_app()
