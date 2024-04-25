from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from common.exception.exception import ElasticsearchException


def elasticsearch_exception_handler(app):
    @app.exception_handler(ElasticsearchException)
    async def elasticsearch_error(request: Request, exc: ElasticsearchException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "response_code": exc.code,
                "response_message": exc.detail
            }
        )


def pydantic_exception_handler(app):
    @app.exception_handler(ValidationError)
    async def pydantic_validation_error(request: Request, exc: RequestValidationError):
        error = exc.errors()[0]
        content = {"response_code": 400, "response_message": f"{error['msg']}"}
        return JSONResponse(status_code=400, content=content)
