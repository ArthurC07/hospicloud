# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from invoice.models import Recibo


class Command(BaseCommand):
    help = "Corrects invoices that do not have legal data"

    def handle(self, *args, **options):
        recibos = Recibo.objects.filter(legal_data__isnull=True)

        [r.asignar_ciudad() for r in recibos]
