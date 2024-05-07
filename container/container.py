from dependency_injector import containers, providers

from core.elasticsearch import ElasticSearchClient, AsyncElasticSearchClient
from app.repository.news_repository import NewsRepository
from app.repository.provider_repository import ProviderRepository
from app.repository.category_repository import CategoryRepository

from app.service.news_service import NewsService
from app.service.provider_service import ProviderService
from app.service.category_service import CategoryService


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])
    es_client = providers.Singleton(ElasticSearchClient)
    async_es_client = providers.Singleton(AsyncElasticSearchClient)

    NewsRepository = providers.Singleton(NewsRepository, es_client=es_client)
    ProviderRepository = providers.Singleton(ProviderRepository, es_client=es_client)
    CategoryRepository = providers.Singleton(CategoryRepository, es_client=es_client)

    NewsService = providers.Singleton(NewsService, news_repository=NewsRepository)
    ProviderService = providers.Singleton(ProviderService, provider_repository=ProviderRepository)
    CategoryService = providers.Singleton(CategoryService, category_repository=CategoryRepository)
