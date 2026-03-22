from calendar import monthrange
from datetime import date, timedelta


def month_bounds(target: date) -> tuple[date, date]:
    start = target.replace(day=1)
    end = target.replace(day=monthrange(target.year, target.month)[1])
    return start, end


def previous_month_bounds(target: date) -> tuple[date, date]:
    first_day = target.replace(day=1)
    previous_day = first_day - timedelta(days=1)
    return month_bounds(previous_day)
