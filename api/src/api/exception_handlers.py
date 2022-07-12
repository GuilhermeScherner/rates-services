import traceback
from typing import Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.services.exceptions.exceptions import AlreadyExists, ErrorCodeEnum, NotFound, Unauthorized



async def already_exists_exception_handler(request: Request, exc: AlreadyExists) -> Response:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": {"message": exc.message, "code": exc.code.value}},
    )


async def not_found_exception_handler(request: Request, exc: NotFound) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": {"message": exc.message, "code": exc.code.value}},
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "validation error",
                "code": ErrorCodeEnum.VALIDATION_ERROR.value,
                "details": exc.errors(),
            }
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "validation error",
                "code": ErrorCodeEnum.VALIDATION_ERROR.value,
                "details": exc.errors(),
            }
        },
    )


async def unauthorized_exception_handler(request: Request, exc: Unauthorized) -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
        content={
            "error": {
                "message": "Not authenticated",
                "code": exc.code.value,
            }
        },
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(AlreadyExists, already_exists_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(Unauthorized, unauthorized_exception_handler)
    app.add_exception_handler(NotFound, not_found_exception_handler)