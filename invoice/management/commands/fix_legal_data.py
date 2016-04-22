# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from invoice.models import Recibo


class Command(BaseCommand):
    help = "Corrects invoices that do not have legal data"

    def handle(self, *args, **options):
        recibos = Recibo.objects.filter(legal_data__isnull=True)

        for recibo in recibos:
            recibo.legal_data = recibo.ciudad.recibo
            recibo.save()
