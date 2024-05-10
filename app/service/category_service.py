import csv
import json

from app.repository.category_repository import CategoryRepository
from app.schema.dto import InsertResponse, MainCategoryResponse
from common.category_enum import CategoryType
from core.config import settings


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def set_category_data(self):
        success_list, fail_list = [], []
        # 카테고리 인덱스
        if not self.category_repository.exists_index(settings.CATEGORY_INDEX_NAME):
            with open(settings.CATEGORY_INDEX_SETTING, 'r', encoding='utf-8') as index_setting_file:
                index_setting = json.load(index_setting_file)
            await self.category_repository.create_index(settings.CATEGORY_INDEX_NAME, index_setting)

            with open(settings.CATEGORY_INDEX_DATA, 'r', encoding='utf-8') as index_data_file:
                reader = csv.DictReader(index_data_file)
                index_data = [row for row in reader]
            success_list, fail_list = self.category_repository.streaming_bulk_insert(settings.CATEGORY_INDEX_NAME,
                                                                                     index_data)
        return InsertResponse(success_count=len(success_list), fail_count=len(fail_list))

    def get_category_list(self, category_type: CategoryType):
        if category_type == CategoryType.SECOND:
            body = {
                "query": {
                    "bool": {
                        "must_not": [
                            {
                                "term": {
                                    "second.keyword": ""
                                }
                            }
                        ]
                    }
                },
                "aggs": {
                    "categories": {
                        "terms": {
                            "field": "first.keyword",
                            "size": 100
                        },
                        "aggs": {
                            "sub_categories": {
                                "terms": {
                                    "field": "second.keyword",
                                    "size": 100
                                }
                            }
                        }
                    }

                }
            }
        elif category_type == CategoryType.THIRD:
            body = {
                "query": {
                    "bool": {
                        "must_not": [
                            {
                                "term": {
                                    "third.keyword": ""
                                }
                            }
                        ]
                    }
                },
                "aggs": {
                    "categories": {
                        "terms": {
                            "field": "second.keyword",
                            "size": 100
                        },
                        "aggs": {
                            "sub_categories": {
                                "terms": {
                                    "field": "third.keyword",
                                    "size": 100
                                }
                            }
                        }
                    }

                }

            }

        else:
            body = {
                "aggs": {
                    "categories": {
                        "terms": {
                            "field": "first.keyword",
                            "size": 100
                        }
                    }
                }
            }
        response = self.category_repository.search(index_name=settings.CATEGORY_INDEX_NAME, body=body, size=0)
        result = response["aggregations"]["categories"]["buckets"]
        return MainCategoryResponse.to_main_category(result, category_type)
