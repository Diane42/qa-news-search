from typing import Optional

from app.repository.provider_repository import ProviderRepository
from common.enums.provider_enum import ProviderType
from core.config import settings


class ProviderService:
    def __init__(self, provider_repository: ProviderRepository):
        self.provider_repository = provider_repository

    def get_provider(self, provider_type: ProviderType, type_name: Optional[str]):
        keyword = provider_type.__str__().lower() + ".keyword"
        if type_name:
            return self.get_provider_name_list_by_type(keyword, type_name)
        else:
            return self.get_provider_type_list(keyword)

    def get_provider_type_list(self, keyword: str):
        response = self.provider_repository.search(index_name=settings.PROVIDER_INDEX_NAME,
                                                   body={
                                                       "aggs": {
                                                           "by_type": {
                                                               "terms": {
                                                                   "field": keyword,
                                                                   "size": 100,
                                                                   "order": {
                                                                       "_key": "asc"
                                                                   }
                                                               }
                                                           }
                                                       }
                                                   },
                                                   size=0)
        return [bucket["key"] for bucket in response["aggregations"]["by_type"]["buckets"]]

    def get_provider_name_list_by_type(self, keyword: str, type_name: str):
        response = self.provider_repository.search(index_name=settings.PROVIDER_INDEX_NAME,
                                                   body={
                                                       "query": {
                                                           "term": {
                                                               keyword: type_name
                                                           }
                                                       },
                                                       "sort": [
                                                           {
                                                               "name.keyword": {
                                                                   "order": "asc"
                                                               }
                                                           }
                                                       ]
                                                   },
                                                   size=500)
        return [doc["_source"]["name"] for doc in response["hits"]["hits"]]
