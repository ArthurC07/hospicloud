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
    previous_month_end = date(inicio.year, inicio.month,
               calendar.monthrange(inicio.year, inicio.month)[1])

    return previous_month_end, previous_month_start
