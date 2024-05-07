from typing import Optional

from fastapi import Query

from app.schema.dto import NewsSearchRequest
from common.enums.news_enum import SortBy, DateRange


def get_news_params(
        keyword: str,
        sort_by: SortBy,
        date_range: DateRange,
        start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
        end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
        provider_name: Optional[str] = Query(None),
        provider_section: Optional[str] = Query(None),
        provider_local: Optional[str] = Query(None),
        provider_abc: Optional[str] = Query(None),
        byline: Optional[str] = Query(None),
        category_1: Optional[str] = Query(None),
        category_2: Optional[str] = Query(None),
        category_3: Optional[str] = Query(None),
        search_after: Optional[list] = Query(None),
        pit_id: Optional[str] = Query(None)
) -> NewsSearchRequest:
    return NewsSearchRequest(
        keyword=keyword,
        sort_by=sort_by,
        date_range=date_range,
        start_date=start_date,
        end_date=end_date,
        provider_name=provider_name,
        provider_section=provider_section,
        provider_local=provider_local,
        provider_abc=provider_abc,
        byline=byline,
        category_1=category_1,
        category_2=category_2,
        category_3=category_3,
        search_after=search_after,
        pit_id=pit_id
    )

