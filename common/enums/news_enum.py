from datetime import datetime, timedelta, time
from enum import auto

from dateutil.relativedelta import relativedelta

from common.enums import StrEnum


class SortBy(StrEnum):
    RELEVANCE = auto()
    NEWEST = auto()
    OLDEST = auto()


class DateRange(StrEnum):
    ALL = auto()
    LAST_1_HOUR = auto()
    LAST_2_HOUR = auto()
    LAST_3_HOUR = auto()
    LAST_4_HOUR = auto()
    LAST_5_HOUR = auto()
    LAST_6_HOURS = auto()
    LAST_1_DAY = auto()
    LAST_1_WEEK = auto()
    LAST_1_MONTH = auto()
    LAST_3_MONTHS = auto()
    LAST_6_MONTHS = auto()
    LAST_1_YEAR = auto()
    CUSTOM = auto()

    def calculate_date_range(self, start_date=None, end_date=None):
        # TODO : 테스트용 시간 설정, 개발 완료 후 datetime.now()으로 변경 예정
        now = datetime(2021, 5, 1, 12, 12, 12)

        if self == DateRange.ALL:
            return None

        periods = {
            DateRange.LAST_1_HOUR: timedelta(hours=1),
            DateRange.LAST_2_HOUR: timedelta(hours=2),
            DateRange.LAST_3_HOUR: timedelta(hours=3),
            DateRange.LAST_1_DAY: timedelta(days=1),
            DateRange.LAST_1_WEEK: timedelta(weeks=1),
            DateRange.LAST_1_MONTH: relativedelta(months=1),
            DateRange.LAST_3_MONTHS: relativedelta(months=3),
            DateRange.LAST_6_MONTHS: relativedelta(months=6),
            DateRange.LAST_1_YEAR: relativedelta(years=1)
        }
        if self in periods:
            delta = periods[self]
            return {"gte": (now - delta).isoformat(), "lte": now.isoformat()}
        elif self == DateRange.CUSTOM:
            if start_date and end_date:
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                start_date_with_time = datetime.combine(start_date, time(0, 0, 0))
                end_date_with_time = datetime.combine(end_date, time(23, 59, 59))
                return {"gte": start_date_with_time.isoformat(), "lte": end_date_with_time.isoformat()}
        return None
