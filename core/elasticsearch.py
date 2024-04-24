from typing import Union
from elasticsearch import Elasticsearch
from core.config import settings


class ElasticSearchClient:
    def __init__(self):
        self.hosts = settings.ES_HOST
        self.client: Union[Elasticsearch, None] = None

    def connect(self):
        self.client = Elasticsearch(settings.ES_URL,
                                    verify_certs=False,
                                    basic_auth=(settings.ES_USER, settings.ES_PASSWORD)
                                    , timeout=60)

        result = self.client.ping()

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

