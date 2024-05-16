from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from app.schema import BasicResponse
from common.category_enum import CategoryType
from common.enums.news_enum import SortBy, DateRange
from common.enums.provider_enum import ProviderGroupType


class NewsDTO(BaseModel):
    score: float
    id: int
    title: list[str]
    content: list[str]
    provider: dict
    byline: Optional[str]
    category: list
    dateline: str
    search_after: list


class NewsSearchRequest(BaseModel):
    q: str
    sort_by: SortBy
    date_range: DateRange
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    provider_name: Optional[str] = None
    provider_section: Optional[str] = None
    provider_local: Optional[str] = None
    provider_abc: Optional[str] = None
    byline: Optional[str] = None
    category_1: Optional[str] = None
    category_2: Optional[str] = None
    category_3: Optional[str] = None
    search_after: Optional[list] = None
    pit_id: Optional[str] = None
    suggest: bool = True

    @model_validator(mode="after")
    def validate(self):
        if self.search_after:
            search_after = []
            for val in self.search_after[0].split(","):
                val = val.strip()
                if val:
                    if '.' in val:
                        val = float(val)
                    elif "\"" in val or "'" in val:
                        val = val.replace("\"", "").replace("'", "")
                    else:
                        val = int(val)
                    print(val)
                    search_after.append(val)
            self.search_after = search_after
        # else:
        #     self.search_after = []
        if self.date_range == DateRange.CUSTOM:
            if self.start_date is None or self.end_date is None:
                raise ValueError('When date range is custom, there must be a start date and an end date.')
            else:
                if self.start_date > self.end_date:
                    self.start_date, self.end_date = self.end_date, self.start_date
                for field in ["start_date", "end_date"]:
                    date_value = getattr(self, field)
                    setattr(self, field, datetime.strptime(date_value, "%Y-%m-%d"))
        else:
            if self.start_date and self.end_date:
                self.date_range = DateRange.CUSTOM

        return self


class InsertResponse(BasicResponse):
    success_count: int
    fail_count: int


class NewsSearchResponse(BasicResponse):
    pit_id: str
    total_count: int
    return_count: int
    request_q: str
    suggest_q: Optional[str]
    news_list: list[NewsDTO]

    @staticmethod
    def to_response(response: dict, request_q: str, suggest_q: Optional[str]=None):
        result = [doc for doc in response['hits']['hits']]
        return NewsSearchResponse(pit_id=response.get("pit_id"),
                                  total_count=response["hits"]["total"]["value"],
                                  return_count=len(result),
                                  request_q=request_q,
                                  suggest_q=suggest_q,
                                  news_list=[NewsDTO(
                                      score=doc["_score"],
                                      id=doc["_source"]["id"],
                                      title=doc["highlight"]['title.ngram'] if 'title.ngram' in doc["highlight"] else doc["_source"]["title"],
                                      content=doc["highlight"]['content.ngram'] if 'content.ngram' in doc["highlight"] else doc["_source"]["content"],
                                      provider=doc["_source"]["provider"],
                                      byline=doc["_source"].get("byline"),
                                      category=doc["_source"]["category"],
                                      dateline=doc["_source"]["dateline"],
                                      search_after=doc["sort"],
                                  ) for doc in result]
                                  )


class ProviderDTO(BaseModel):
    provider_type: str
    provider_count: int
    provider_list: list[str]


class ProviderListResponse(BasicResponse):
    group_type: ProviderGroupType
    group_count: int
    group_list: list[ProviderDTO]

    @staticmethod
    def to_response(provider_type: ProviderGroupType, get_results: list):
        return ProviderListResponse(group_type=provider_type,
                                    group_count=len(get_results),
                                    group_list=(ProviderDTO(
                                        provider_type=result["key"],
                                        provider_count=len(result["provider_names"]["buckets"]),
                                        provider_list=[provider["key"] for provider in
                                                       result["provider_names"]["buckets"]]
                                    ) for result in get_results
                                    )
                                    )


class CategoryDto(BaseModel):
    main: Optional[str]
    sub: list[str]


class MainCategoryResponse(BasicResponse):
    category_list: list[CategoryDto]

    @staticmethod
    def to_main_category(get_results: list, category_type: CategoryType):
        if category_type == CategoryType.FIRST:
            return MainCategoryResponse(
                category_list=[CategoryDto(
                    main=None,
                    sub=[result["key"] for result in get_results]
                )]
            )
        else:
            return MainCategoryResponse(
                category_list=(CategoryDto(
                    main=result["key"],
                    sub=[doc["key"] for doc in result["sub_categories"]["buckets"]]
                    ) for result in get_results
                )
            )


