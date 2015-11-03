# -*- coding: utf-8 -*-
import calendar
from datetime import date, datetime, time

from dateutil.relativedelta import relativedelta
from django.utils import timezone


def get_current_month_range():
    now = timezone.now()
    fin = date(now.year, now.month,
               calendar.monthrange(now.year, now.month)[1])
    inicio = date(now.year, now.month, 1)
    fin = datetime.combine(fin, time.max)
    inicio = datetime.combine(inicio, time.min)
    fin = timezone.make_aware(fin, timezone.get_current_timezone())
    inicio = timezone.make_aware(inicio,
                                 timezone.get_current_timezone())
    return fin, inicio


def get_previous_month_range():
    fin, inicio = get_current_month_range()
    previous_month_start = inicio - relativedelta(months=1)
    previous_month_end = date(previous_month_start.year,
                              previous_month_start.month,
                              calendar.monthrange(previous_month_start.year,
                                                  previous_month_start.month)[
                                  1])
    previous_month_end = datetime.combine(previous_month_end, time.max)
    previous_month_end = timezone.make_aware(previous_month_end,
                                             timezone.get_current_timezone())

    return previous_month_end, previous_month_start


def make_end_day(day):

    day = datetime(day.year, day.month, day.day, 23, 59, 59)
    return timezone.make_aware(day, timezone.get_current_timezone())
