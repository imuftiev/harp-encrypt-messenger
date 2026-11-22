import uuid
from fastapi.middleware import Middleware
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

middleware_ = Middleware


async def add_process_time_header(request: Request, call_next) -> JSONResponse:
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def register_middleware(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
