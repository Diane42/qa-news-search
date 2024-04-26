from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from common.enums.news_enum import SortBy, DateRange


class NewsSearchRequest(BaseModel):
    keyword: str
    sort_by: SortBy
    date_range: DateRange
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    provider: list[str] = []
    byline: Optional[str] = None

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

        return self
