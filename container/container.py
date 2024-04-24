from dependency_injector import containers, providers

from core.elasticsearch import ElasticSearchClient


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])
    es_client = providers.Singleton(ElasticSearchClient)

