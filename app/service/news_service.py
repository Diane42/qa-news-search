import csv
import json

from app.repository.news_repository import NewsRepository
from app.schema import BasicResponse
from app.schema.news_dto import NewsSearchRequest
from common.enums.news_enum import SortBy
from core.config import settings


class NewsService:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    async def set_bulk_data(self, index_name: str, index_path: str, csv_path: str):
        with open(index_path, 'r', encoding='utf-8') as index_data:
            index_body = json.load(index_data)
        await self.news_repository.create_index(index_name, index_body)

        with open(csv_path, 'r', encoding='utf-8') as csv_data:
            reader = csv.DictReader(csv_data)
            docs = []
            for row in reader:
                filtered_row = {key: value for key, value in row.items() if value.strip()}
                docs.append({"index": {
                    "_index": index_name,
                    "_type": "_doc"
                }})
                docs.append(filtered_row)
        await self.news_repository.bulk_insert(docs)

    async def set_news_data(self):
        if not self.news_repository.exists_index(settings.PROVIDER_INDEX_NAME):
            await self.set_bulk_data(index_name=settings.PROVIDER_INDEX_NAME,
                                     index_path=settings.PROVIDER_INDEX_SETTING,
                                     csv_path=settings.PROVIDER_INDEX_CSV)

        if not self.news_repository.exists_index(settings.NEWS_INDEX_NAME):
            await self.set_bulk_data(index_name=settings.NEWS_INDEX_NAME,
                                     index_path=settings.NEWS_INDEX_SETTING,
                                     csv_path=settings.NEWS_INDEX_CSV)

        return BasicResponse()

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
