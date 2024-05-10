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
        return InsertResponse(success_count=len(success_list), fail_count=len(fail_list))

    def search_news(self, request: NewsSearchRequest):
        # TODO : now로 변경 (해당 일자는 .csv 뉴스 데이터의 가장 마지막 일자)
        origin_date = "2021-10-01"

        # 기간
        filter_list = []
        date_filter = request.date_range.calculate_date_range(request.start_date, request.end_date)
        if date_filter:
            filter_list.append({"range": {"dateline": {"gte": date_filter.get("gte"), "lte": date_filter.get("lte")}}})
            if 'origin' in date_filter and date_filter['origin'] < origin_date:
                origin_date = date_filter['origin']

        must_list = [{
            "function_score": {
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"title.nori": {"query": request.q, "boost": 3}}},
                            {"match": {"content.nori": {"query": request.q, "boost": 2}}}
                        ]
                    }
                },
                "functions": [
                    {
                        "gauss": {
                            "dateline": {
                                "origin": origin_date,
                                "scale": "7d",
                                "offset": "0d",
                                "decay": 0.5
                            }
                        }
                    }
                ],
                "score_mode": "sum",
                "boost_mode": "multiply",
                "boost": 2
            }
        }]

        # 언론사
        if request.provider_name:
            must_list.append({"match": {"provider.name.ngram": {"query": request.provider_name}}})
        if request.provider_section:
            must_list.append({"match": {"provider.section.ngram": {"query": request.provider_section}}})
        if request.provider_local:
            must_list.append({"match": {"provider.local.ngram": {"query": request.provider_local}}})
        if request.provider_abc:
            must_list.append({"match": {"provider.abc.ngram": {"query": request.provider_abc}}})

        # 카테고리
        if request.category_1:
            must_list.append({"match": {"category.first.ngram": {"query": request.category_1}}})
        if request.category_2:
            must_list.append({"match": {"category.second.ngram": {"query": request.category_2}}})
        if request.category_3:
            must_list.append({"match": {"category.third.ngram": {"query": request.category_3}}})

        # 기자명
        if request.byline:
            must_list.append({"match": {"byline.ngram": {"query": request.byline}}})

        # 정렬
        sort_list = [{"_score": {"order": "desc"}}]
        if request.sort_by == SortBy.NEWEST:
            sort_list.insert(0, {"dateline": {"order": "desc"}})
        elif request.sort_by == SortBy.OLDEST:
            sort_list.insert(0, {"dateline": {"order": "asc"}})
        elif request.sort_by == SortBy.RELEVANCE:
            sort_list.append({"dateline": {"order": "desc"}})

        highlight_dict = {
            "fields": {
                "title.ngram": {
                    "fragment_size": 50,
                    "number_of_fragments": 1,
                    "no_match_size": 50,
                    "highlight_query": {
                        "bool": {
                            "must": {
                                "match": {
                                    "title.ngram": {
                                        "query": request.q
                                    }
                                }
                            }
                        }
                    }
                },
                "content.ngram": {
                    "fragment_size": 100,
                    "number_of_fragments": 2,
                    "no_match_size": 100,
                    "highlight_query": {
                        "bool": {
                            "must": {
                                "match": {
                                    "content.ngram": {
                                        "query": request.q
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "pre_tags": ["<mark>"],
            "post_tags": ["</mark>"]
        }
        body = {
            "query": {
                "bool": {
                    "should": [{
                        "match": {
                            "title.ngram": {
                                "query": request.q,
                                "boost": 5
                            }
                        }
                    },
                        {
                            "match": {
                                "content.ngram": {
                                    "query": request.q,
                                    "boost": 5
                                }
                            }
                        }],
                    "must": must_list,
                    "filter": filter_list
                }
            },
            "sort": sort_list,
            "highlight": highlight_dict
        }
        if request.search_after:
            body["search_after"] = request.search_after

        if request.pit_id:
            body["pit"] = {"id": request.pit_id, "keep_alive": "1m"}
        else:
            created_pit = self.news_repository.create_pit(index_name=settings.NEWS_INDEX_NAME)
            body["pit"] = {"id": created_pit["id"], "keep_alive": "1m"}

        response = self.news_repository.search(index_name=settings.NEWS_INDEX_NAME, body=body, size=10)

        return NewsSearchResponse.to_response(response)
