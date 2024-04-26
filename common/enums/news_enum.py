from datetime import datetime, timedelta, time
from enum import auto

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
        #TODO : 테스트용 시간 설정, 개발 완료 후 datetime.now()으로 변경 예정
        now = datetime(2021, 5, 1, 12, 00, 00)

        if self == DateRange.ALL:
            return None
        elif self in [DateRange.LAST_1_HOUR, DateRange.LAST_2_HOUR, DateRange.LAST_3_HOUR,
                      DateRange.LAST_4_HOUR, DateRange.LAST_5_HOUR, DateRange.LAST_6_HOURS]:
            hours = int(self.name.split('_')[-2])
            return {"gte": now - timedelta(hours=hours), "lte": now}
        elif self == DateRange.LAST_1_DAY:
            return {"gte": now - timedelta(days=1), "lte": now}
        elif self == DateRange.LAST_1_WEEK:
            return {"gte": now - timedelta(weeks=1), "lte": now}
        elif self == DateRange.LAST_1_MONTH:
            return {"gte": now - timedelta(days=30), "lte": now}
        elif self == DateRange.LAST_3_MONTHS:
            return {"gte": now - timedelta(days=90), "lte": now}
        elif self == DateRange.LAST_6_MONTHS:
            return {"gte": now - timedelta(days=180), "lte": now}
        elif self == DateRange.LAST_1_YEAR:
            return {"gte": now - timedelta(days=365), "lte": now}
        elif self == DateRange.CUSTOM:
            if start_date and end_date:
                if isinstance(end_date, datetime):
                    end_date_with_time = end_date.replace(hour=23, minute=59, second=59)
                else:
                    end_date_with_time = datetime.combine(end_date, time(23, 59, 59))

                return {"gte": start_date, "lte": end_date_with_time}
        else:
            return None
