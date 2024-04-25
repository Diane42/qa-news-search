from datetime import datetime
from typing import Optional

from fastapi import Query

from common.enums.news_enum import SortBy, DateRange
from app.schema.news_dto import NewsSearchRequest


def get_news_params(
        sort_by: SortBy,
        date_range: DateRange,
        start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
        end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),

) -> NewsSearchRequest:
    return NewsSearchRequest(
        sort_by=sort_by,
        date_range=date_range,
        start_date=start_date,
        end_date=end_date
    )
