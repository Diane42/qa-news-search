from fastapi import FastAPI
from container.container import AppContainer
from app.router.news import router as news_router
from app.router.provider import router as provider_router
from core.exception_handler import elasticsearch_exception_handler, pydantic_exception_handler


def create_app():
    app = FastAPI()
    container = AppContainer()
    container.wire(packages=["app"])
    app.container = container

    @app.on_event("startup")
    async def startup_event():
        container.es_client().connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        container.es_client().close()

    app.include_router(news_router, tags=["news"])
    app.include_router(provider_router, tags=["provider"])

    elasticsearch_exception_handler(app)
    pydantic_exception_handler(app)

    return app


news_app = create_app()
