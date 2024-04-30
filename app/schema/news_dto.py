from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from app.schema import BasicResponse
from common.enums.news_enum import SortBy, DateRange


class NewsDTO(BaseModel):
    score: float
    id: int
    title: str
    content: str
    provider: str
    byline: Optional[str]
    category: list[dict]
    dateline: str


class NewsSearchRequest(BaseModel):
    keyword: str
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

    @model_validator(mode="after")
    def validate(self):
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


class NewsInsertResponse(BasicResponse):
    success_list: list[str]
    fail_list: list[str]


class NewsSearchResponse(BasicResponse):
    return_cnt: int
    news_list: list[NewsDTO]

    @staticmethod
    def to_response(search_results: list):
        return NewsSearchResponse(return_cnt=len(search_results),
                                  news_list=(NewsDTO
                                             (score=result["_score"],
                                              id=result["_source"]["id"],
                                              title=result["_source"]["title"],
                                              content=result["_source"]["content"][:100] + "...",
                                              provider=result["_source"]["provider"]["name"],
                                              byline=result["_source"]["byline"] if result["_source"]["byline"] else None,
                                              category=result["_source"]["category"],
                                              dateline=result["_source"]["dateline"]
                                              ) for result in search_results
                                             )
                                  )
