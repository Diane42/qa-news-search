from dependency_injector import containers, providers

from core.elasticsearch import ElasticSearchClient
from app.repository.news_repository import NewsRepository

from app.service.news_service import NewsService


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])
    es_client = providers.Singleton(ElasticSearchClient)

    NewsRepository = providers.Singleton(NewsRepository, es_client=es_client)

    NewsService = providers.Singleton(NewsService, news_repository=NewsRepository)
