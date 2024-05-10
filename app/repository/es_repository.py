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

    def streaming_bulk_insert(self, index_name: str, data: list):
        return self.es_client.streaming_bulk_insert(index_name, data)

    def create_pit(self, index_name: str):
        return self.es_client.create_pit(index_name)

    def delete_pit(self, pit_id: str):
        return self.es_client.delete_pit(pit_id)

    def search(self, index_name: str, body: dict, size: int):
        return self.es_client.search(index_name, body, size)

    def scroll(self, scroll_id: str, scroll: str):
        return self.es_client.scroll(scroll_id=scroll_id, scroll=scroll)

