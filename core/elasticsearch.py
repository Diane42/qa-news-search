import json
from typing import Union
from elasticsearch import Elasticsearch
from common.exception.exception import ElasticsearchException
from core.config import settings


class ElasticSearchClient:
    def __init__(self):
        self.hosts = settings.ES_HOST
        self.client: Union[Elasticsearch, None] = None

    def connect(self):
        self.client = Elasticsearch(settings.ES_URL,
                                    verify_certs=False,
                                    basic_auth=(settings.ES_USER, settings.ES_PASSWORD)
                                    , timeout=600)

        result = self.client.ping()

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def create_index(self, index_name: str, body: dict):
        try:
            self.client.indices.create(index=index_name, body=body)
        except Exception as e:
            raise ElasticsearchException(code=500, detail=str(e))

    def delete_index(self, index_name: str):
        return self.client.indices.delete(index=index_name)

    def exists_index(self, index_name: str):
        return self.client.indices.exists(index=index_name)

    def bulk_insert(self, body: list[dict]):
        result = self.client.bulk(body=body)
        if result.get('errors'):
            error_detail = json.dumps(result)
            raise ElasticsearchException(code=500, detail=str(error_detail))
        return result
