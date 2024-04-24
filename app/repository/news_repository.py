from core.elasticsearch import ElasticSearchClient


class NewsRepository:
    def __init__(self, es_client: ElasticSearchClient):
        self.es_client = es_client

