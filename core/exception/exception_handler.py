import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .exceptions import AppError, NotFoundError, ConflictError, ForbiddenError

logger = logging.getLogger(__name__)

# HTTP-статусы живут только здесь, домен о них не знает
STATUS_MAP: dict[type[AppError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
    ForbiddenError: status.HTTP_403_FORBIDDEN,
    AppError: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def _resolve_status(exc: AppError) -> int:
    for cls in type(exc).__mro__:
        if cls in STATUS_MAP:
            return STATUS_MAP[cls]
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def _response(request: Request, status_code: int, code: str, message: str, details=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_code = _resolve_status(exc)
    if status_code >= 500:
        logger.exception("Application error", exc_info=exc)
    return _response(request, status_code, exc.code, exc.message, exc.details or None)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _response(
        request, 422, "validation_error", "Request validation failed", exc.errors()
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _response(request, exc.status_code, "http_error", str(exc.detail))


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    return _response(request, 500, "internal_error", "Internal server error")


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
