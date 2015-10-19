import calendar
from datetime import date, datetime, time

from dateutil.relativedelta import relativedelta
from django.utils import timezone

cache = {}


def make_day_start(day):
    inicio = date(day.year, day.month, 1)
    inicio = datetime.combine(inicio, time.min)
    return inicio


def make_end_day(day):
    day = datetime.combine(day, time.max)
    return timezone.make_aware(day, timezone.get_current_timezone())


def get_current_month_range():
    now = timezone.now()
    month = now.month

    if 'inicio' not in cache or 'fin' not in cache or cache[
        'inicio'].month != month or cache['fin'].month != month:
        fin = date(now.year, now.month,
                   calendar.monthrange(now.year, now.month)[1])
        inicio = make_day_start(now)
        cache['fin'] = make_end_day(fin)
        cache['inicio'] = timezone.make_aware(inicio,
                                              timezone.get_current_timezone())
    return cache['fin'], cache['inicio']


def get_previous_month_range():
    fin, inicio = get_current_month_range()
    previous_month_start = inicio - relativedelta(months=1)
    previous_month_end = date(previous_month_start.year,
                              previous_month_start.month,
                              calendar.monthrange(previous_month_start.year,
                                                  previous_month_start.month)[
                                  1])
    previous_month_end = make_end_day(previous_month_end)

    return previous_month_end, previous_month_start
