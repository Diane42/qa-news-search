from typing import Optional

from core.elasticsearch import ElasticSearchClient


class ESRepository:
    def __init__(self, es_client: ElasticSearchClient):
        self.es_client = es_client

    async def create_index(self, index_name: str, body: dict):
        return self.es_client.create_index(index_name, body)

    def delete_index(self, index_name: str):
        return self.es_client.delete_index(index_name)

    def exists_index(self, index_name: str):
        return self.es_client.exists_index(index_name)

    async def bulk_insert(self, body: list[dict]):
        return self.es_client.bulk_insert(body)

    def search(self, index_name: str, body: dict, size: int, scroll: Optional[str] = None):
        return self.es_client.search(index_name, body, size, scroll)

    def scroll(self, scroll_id: str, scroll: str):
        return self.es_client.scroll(scroll_id, scroll)
