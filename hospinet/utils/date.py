# -*- coding: utf-8 -*-
import calendar
from datetime import date, datetime, time

from dateutil.relativedelta import relativedelta
from django.utils import timezone

cache = {}


def make_day_start(day):
    inicio = datetime.combine(day.date(), time.min)
    inicio = timezone.make_aware(inicio, timezone.get_current_timezone())
    return inicio


def make_end_day(day):
    day = datetime.combine(day, time.max)
    return timezone.make_aware(day, timezone.get_current_timezone())


def get_month_end(day):
    return date(
        day.year,
        day.month,
        calendar.monthrange(day.year, day.month)[1]
    )


def make_month_range(start):
    day = start.replace(day=1)
    fin = make_end_day(get_month_end(day))
    inicio = make_day_start(day)
    return inicio, fin


def get_current_month_range():
    now = timezone.now()
    now = now.replace(day=1)

    if 'inicio' not in cache or 'fin' not in cache or cache[
        'inicio'].month != now.month or cache['fin'].month != now.month:
        fin = get_month_end(now)
        cache['fin'] = make_end_day(fin)
        cache['inicio'] = make_day_start(now)
    return cache['fin'], cache['inicio']


def get_previous_month_range():
    fin, inicio = get_current_month_range()
    previous_month_start = inicio - relativedelta(months=1)
    previous_month_end = get_month_end(previous_month_start)
    previous_month_end = make_end_day(previous_month_end)

    return previous_month_end, previous_month_start
