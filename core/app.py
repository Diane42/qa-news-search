from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from common.exception.exception import ElasticsearchException
from container.container import AppContainer


def create_app():
    app = FastAPI()
    container = AppContainer()
    container.wire(packages=["app"])
    app.container = container

    @app.exception_handler(ElasticsearchException)
    async def elasticsearch_exception_handler(request: Request, exc: ElasticsearchException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "response_code": exc.code,
                "response_message": exc.detail
            }
        )

    @app.on_event("startup")
    async def startup_event():
        container.es_client().connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        container.es_client().close()

    return app


news_app = create_app()
