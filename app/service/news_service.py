import json

from app.repository.news_repository import NewsRepository
from app.schema.news_dto import NewsSearchRequest, NewsInsertResponse
from common.enums.news_enum import SortBy
from core.config import settings


class NewsService:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    async def set_index_data(self):
        success_list, fail_list = [], []
        if not self.news_repository.exists_index(settings.NEWS_INDEX_NAME):
            with open(settings.NEWS_INDEX_SETTING, 'r', encoding='utf-8') as index_setting_file:
                index_setting = json.load(index_setting_file)
            await self.news_repository.create_index(settings.NEWS_INDEX_NAME, index_setting)

            with open(settings.NEWS_INDEX_DATA, 'r', encoding='utf-8') as index_data_file:
                index_data = json.load(index_data_file)
            success_list, fail_list = await self.news_repository.streaming_bulk_insert(settings.NEWS_INDEX_NAME, index_data)
        return NewsInsertResponse(success_list=success_list, fail_list=fail_list)

    # TODO: 검색 쿼리 성능, 효율 개선
    def search_news(self, request: NewsSearchRequest):
        must_dicts = [{"match": {"title": request.keyword}}]
        should_dict = []
        minimum_should_match = 0

        if request.provider:
            should_dict = [{"term": {"provider.keyword": name}} for name in request.provider]
            minimum_should_match = 1
        if request.byline:
            must_dicts.append({"match": {"byline": request.byline}})

        sort_criteria = [{"_score": {"order": "desc"}}]
        if request.sort_by == SortBy.NEWEST:
            sort_criteria.insert(0, {"dateline": {"order": "desc"}})
        elif request.sort_by == SortBy.OLDEST:
            sort_criteria.insert(0, {"dateline": {"order": "asc"}})

        body = {
            "query": {
                "bool": {
                    "must": must_dicts,
                    "should": should_dict,
                    "minimum_should_match": minimum_should_match,
                    "filter": []
                }
            },
            "sort": sort_criteria
        }

        date_filter = request.date_range.calculate_date_range(request.start_date, request.end_date)
        if date_filter:
            body["query"]["bool"]["filter"].append({
                "range": {
                    "dateline": date_filter
                }
            })
        response = self.news_repository.search(settings.NEWS_INDEX_NAME, size=100, body=body)
        return [doc for doc in response['hits']['hits']]
