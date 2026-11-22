import uuid
from typing import Any

from fastapi.middleware import Middleware
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

middleware_ = Middleware


async def add_jwt_token() -> Any:
    pass


async def add_request_id(request: Request, call_next) -> JSONResponse:
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def register_middleware(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=add_request_id)
