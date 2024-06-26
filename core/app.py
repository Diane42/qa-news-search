from fastapi import FastAPI
from container.container import AppContainer
from app.router.news import router as news_router
from app.router.provider import router as provider_router
from app.router.category import router as category_router
from core.exception_handler import elasticsearch_exception_handler, pydantic_exception_handler


def create_app():
    app = FastAPI(title="News Search - Diane")
    container = AppContainer()
    container.wire(packages=["app"])
    app.container = container

    @app.on_event("startup")
    async def startup_event():
        container.es_client().connect()
        await container.async_es_client().connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        container.es_client().close()
        await container.async_es_client().connect()

    app.include_router(news_router, tags=["news"])
    app.include_router(provider_router, tags=["provider"])
    app.include_router(category_router, tags=["category"])

    elasticsearch_exception_handler(app)
    pydantic_exception_handler(app)

    return app


news_app = create_app()
