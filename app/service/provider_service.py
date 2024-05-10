import csv
import json

from app.repository.provider_repository import ProviderRepository
from app.schema.dto import InsertResponse, ProviderListResponse
from common.enums.provider_enum import ProviderGroupType
from core.config import settings


class ProviderService:
    def __init__(self, provider_repository: ProviderRepository):
        self.provider_repository = provider_repository

    async def set_provider_data(self):
        success_list, fail_list = [], []
        # 언론사 인덱스
        if not self.provider_repository.exists_index(settings.PROVIDER_INDEX_NAME):
            with open(settings.PROVIDER_INDEX_SETTING, 'r', encoding='utf-8') as index_setting_file:
                index_setting = json.load(index_setting_file)
            await self.provider_repository.create_index(settings.PROVIDER_INDEX_NAME, index_setting)

            with open(settings.PROVIDER_INDEX_DATA, 'r', encoding='utf-8') as index_data_file:
                reader = csv.DictReader(index_data_file)
                index_data = [row for row in reader]
            success_list, fail_list = self.provider_repository.streaming_bulk_insert(settings.PROVIDER_INDEX_NAME,
                                                                                     index_data)
        return InsertResponse(success_count=len(success_list), fail_count=len(fail_list))

    def get_provider_list(self, provider_type: ProviderGroupType):
        field_keyword = provider_type.__str__().lower() + ".keyword"
        response = self.provider_repository.search(index_name=settings.PROVIDER_INDEX_NAME,
                                                   body={
                                                       "query": {
                                                           "bool": {
                                                               "must_not": {
                                                                   "terms": {
                                                                       field_keyword: [""]
                                                                   }
                                                               }
                                                           }
                                                       },
                                                       "aggs": {
                                                           "provider_groups": {
                                                               "terms": {
                                                                   "field": field_keyword,
                                                                   "size": 1000,
                                                                   "order": {
                                                                       "_key": "asc"
                                                                   }
                                                               },
                                                               "aggs": {
                                                                   "provider_names": {
                                                                       "terms": {
                                                                           "field": "name.keyword",
                                                                           "size": 1000,
                                                                           "order": {
                                                                               "_key": "asc"
                                                                           }
                                                                       }
                                                                   }
                                                               }
                                                           }
                                                       }
                                                   },
                                                   size=0
                                                   )
        result = response["aggregations"]["provider_groups"]["buckets"]
        return ProviderListResponse.to_response(provider_type, result)
