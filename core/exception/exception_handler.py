from fastapi import status, FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.exception.exceptions import AppError, ConflictError

STATUS_CODE: dict[type[AppError], int] = {
    ConflictError: status.HTTP_409_CONFLICT,
    AppError: status.HTTP_500_INTERNAL_SERVER_ERROR
}


def _resolve_status_code(exc: AppError) -> int:
    for cls in type(exc).__mro__:
        if cls in STATUS_CODE:
            return STATUS_CODE[cls]
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def _response(request: Request, exc: AppError) -> JSONResponse:
    status_code = _resolve_status_code(exc)
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "request_id": getattr(request.state, "request_id", None),
                "code": exc.code,
                "message": exc.message
            }
        }
    )


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return _response(request, exc)


def register_exception_handler(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
