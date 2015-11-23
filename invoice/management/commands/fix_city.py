from django.core.management.base import BaseCommand

from invoice.models import Recibo


def corregir_recibo(recibo):
    print(recibo)
    recibo.asignar_ciudad()
    recibo.crear_correlativo()
    recibo.save()


class Command(BaseCommand):
    help = "Corrects invoices with 0 as correlative."

    def handle(self, *args, **options):
        recibos = Recibo.objects.filter(
            ciudad__isnull=True, cajero__isnull=False
        )

        [corregir_recibo(r) for r in recibos.all()]
