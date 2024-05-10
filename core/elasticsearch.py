import json
from typing import Optional
from elasticsearch import Elasticsearch, AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import streaming_bulk

from common.exception.exception import ElasticsearchException
from core.config import settings


class ElasticSearchClient:
    def __init__(self):
        self.hosts = settings.ES_HOST
        self.client: Optional[Elasticsearch] = None

    def connect(self):
        self.client = Elasticsearch(settings.ES_HOST,
                                    verify_certs=False,
                                    basic_auth=(settings.ES_USER, settings.ES_PASSWORD)
                                    , timeout=60)

        result = self.client.ping()
        #print("ElasticSearchClient", result)

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

    def streaming_bulk_insert(self, index_name: str, data: list):
        def gen_date(index_name, _sources):
            for _source in _sources:
                doc = {
                    "_index": index_name,
                    "_source": _source
                }
                if "_id" in _source:
                    _id = _source.get("_id")
                    doc['_id'] = _id
                    del _source["_id"]

                yield doc

        success_list = []
        fail_list = []
        for ok, result in streaming_bulk(
                self.client,
                gen_date(index_name, data),
                index=index_name
        ):
            action, result = result.popitem()
            if not ok:
                fail_list.append(result.get('_id'))
            else:
                success_list.append(result.get('_id'))

        return success_list, fail_list

    def create_pit(self, index_name: str):
        return self.client.open_point_in_time(index=index_name, keep_alive="1m")

    def delete_pit(self, pit_id: str):
        return self.client.close_point_in_time(id=pit_id)

    def search(self, index_name: str, body: dict, size: int):
        try:
            if 'pit' in body:
                body['size'] = size
                try:
                    return self.client.search(body=body)
                except NotFoundError as e:
                    if "No search context found for id" in str(e):
                        body['pit'] = {"id": self.create_pit(index_name)["id"], "keep_alive": "1m"}
                        return self.client.search(body=body)
                    else:
                        raise ElasticsearchException(code=500, detail=str(e))
            else:
                body['size'] = size
                return self.client.search(index=index_name, body=body)
        except Exception as e:
            raise ElasticsearchException(code=500, detail=str(e))

    def scroll(self, scroll_id: str, scroll: str):
        return self.client.scroll(scroll_id=scroll_id, scroll=scroll)


class AsyncElasticSearchClient:
    def __init__(self):
        self.hosts = settings.ES_HOST
        self.client: Optional[AsyncElasticsearch] = None

    async def connect(self):
        self.client = AsyncElasticsearch(settings.ES_HOST,
                                         basic_auth=(settings.ES_USER, settings.ES_PASSWORD)
                                         , timeout=60)

        result = await self.client.ping()
        #print("AsyncElasticSearchClient", result)

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
