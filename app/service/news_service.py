import json

from app.repository.news_repository import NewsRepository
from app.schema.dto import NewsSearchRequest, InsertResponse, NewsSearchResponse
from common.enums.news_enum import SortBy
from core.config import settings


class NewsService:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    async def set_news_data(self):
        success_list, fail_list = [], []
        if not self.news_repository.exists_index(settings.NEWS_INDEX_NAME):
            with open(settings.NEWS_INDEX_SETTING, 'r', encoding='utf-8') as index_setting_file:
                index_setting = json.load(index_setting_file)
            await self.news_repository.create_index(settings.NEWS_INDEX_NAME, index_setting)

            with open(settings.NEWS_INDEX_DATA, 'r', encoding='utf-8') as index_data_file:
                index_data = json.load(index_data_file)
            success_list, fail_list = self.news_repository.streaming_bulk_insert(settings.NEWS_INDEX_NAME, index_data)
        return InsertResponse(success_cnt=len(success_list), fail_cnt=len(fail_list))

    # TODO: 검색 쿼리 성능, 효율 개선
    def search_news(self, request: NewsSearchRequest):
        # 기본 키워드
        must_dicts = [{"multi_match": {
                "query": request.keyword,
                "fields": ["title", "content"],
                "type": "best_fields"
            }
        }]

        # 언론사
        provider_must = []
        if request.provider_name:
            provider_must.append({"match": {"provider.name": request.provider_name}})
        if request.provider_section:
            provider_must.append({"match": {"provider.section": request.provider_section}})
        if request.provider_local:
            provider_must.append({"match": {"provider.local": request.provider_local}})
        if request.provider_abc:
            provider_must.append({"match": {"provider.abc": request.provider_abc}})
        if provider_must:
            must_dicts.append({
                "nested": {
                    "path": "provider",
                    "query": {
                        "bool": {
                            "must": provider_must
                        }
                    }
                }
            })

        # 카테고리
        category_must = []
        if request.category_1:
            category_must.append({"match": {"category.first": request.category_1}})
        if request.category_2:
            category_must.append({"match": {"category.second": request.category_2}})
        if request.category_3:
            category_must.append({"match": {"category.third": request.category_3}})
        if category_must:
            must_dicts.append({
                "nested": {
                    "path": "category",
                    "query": {
                        "bool": {
                            "must": category_must
                        }
                    }
                }
            })

        # 기자명
        if request.byline:
            must_dicts.append({"match": {"byline": request.byline}})

        # 정렬
        sort_criteria = [{"_score": {"order": "desc"}}]
        if request.sort_by == SortBy.NEWEST:
            sort_criteria.insert(0, {"dateline": {"order": "desc"}})
        elif request.sort_by == SortBy.OLDEST:
            sort_criteria.insert(0, {"dateline": {"order": "asc"}})

        # 기간
        filter_list = []
        date_filter = request.date_range.calculate_date_range(request.start_date, request.end_date)
        if date_filter:
            filter_list.append({"range": {"dateline": date_filter}})

        body = {
            "query": {
                "bool": {
                    "must": must_dicts,
                    "filter": filter_list
                }
            },
            "sort": sort_criteria,
            "highlight": {
                "fields": {
                    "title": {},
                    "content": {}
                },
                "pre_tags": ["<mark>"],
                "post_tags": ["</mark>"]
            }
        }

        response = self.news_repository.search(settings.NEWS_INDEX_NAME, size=100, body=body)
        result = [doc for doc in response['hits']['hits']]
        return NewsSearchResponse.to_response(result)

