# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
from collections import defaultdict
from decimal import Decimal
from datetime import timedelta

from constance import config
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from django.db.models import F, Sum

from persona.fields import ColorField
from persona.models import Persona, persona_consolidation_functions
from inventory.models import ItemTemplate, TipoVenta
from spital.models import Deposito
from users.models import Ciudad

dot01 = Decimal("0.01")


class TipoPago(TimeStampedModel):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    color = ColorField(default='')

    def __unicode__(self):
        return self.nombre


class StatusPago(TimeStampedModel):
    nombre = models.CharField(max_length=255, blank=True)
    reportable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

    def total(self):
        total = Pago.objects.filter(status=self).aggregate(
            total=Sum('monto')
        )['total']
        if not total:
            return Decimal()
        return total


class Recibo(TimeStampedModel):
    """Permite registrar pagos por productos y servicios"""

    class Meta:
        permissions = (
            ('cajero', 'Permite al usuario gestionar caja'),
        )

    cliente = models.ForeignKey(Persona, related_name='recibos')
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True,
                               related_name='recibos')
    cajero = models.ForeignKey(User, blank=True, null=True,
                               related_name='recibos')
    tipo_de_venta = models.ForeignKey(TipoVenta, blank=True, null=True)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    correlativo = models.IntegerField(default=0)
    credito = models.BooleanField(default=False)
    cerrado = models.BooleanField(default=False)
    nulo = models.BooleanField(default=False)
    emision = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.id])

    def vencimiento(self):

        return self.emision + timedelta(days=config.RECEIPT_DAYS)

    def facturacion(self):

        return self.created - relativedelta(months=1)

    def total(self):

        total = self.ventas.aggregate(total=Sum('total'))['total']
        if not total:
            return Decimal()
        return total

    @property
    def numero(self):
        ciudad = self.ciudad
        if ciudad is None:
            if self.cajero is None or self.cajero.profile is None or \
                            self.cajero.profile.ciudad is None:
                return self.correlativo

            ciudad = self.cajero.profile.ciudad

        return u'{0}-{1:08d}'.format(ciudad.prefijo_recibo, self.correlativo)

    def other_currency(self):

        return (self.total() / Decimal(config.CURRENCY_EXCHANGE)).quantize(
            Decimal("0.01"))

    def impuesto_other(self):

        return (self.impuesto() / Decimal(config.CURRENCY_EXCHANGE)).quantize(
            Decimal("0.01"))

    def descuento_other(self):

        return (self.descuento() / Decimal(config.CURRENCY_EXCHANGE)).quantize(
            Decimal("0.01"))

    def subtotal_other(self):

        return (self.subtotal() / Decimal(config.CURRENCY_EXCHANGE)).quantize(
            Decimal("0.01"))

    def anular(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""

        self.nulo = True

        for venta in Venta.objects.filter(recibo=self):
            venta.delete()

        for pago in Pago.objects.filter(recibo=self).all():
            pago.delete()
        self.save()

    def cerrar(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""
        if self.pagado() == self.total():
            self.cerrado = True
            self.save()

    def __unicode__(self):

        """Crea una representación en texto del :class:`Recibo`"""

        if self.nulo:
            return u'{0} **NULO**'.format(self.cliente.nombre_completo())

        return self.cliente.nombre_completo()

    def subtotal(self):

        """Calcula el monto antes de impuestos"""

        return \
            self.ventas.aggregate(
                total=Sum('monto', output_field=models.DecimalField()))['total']

    def impuesto(self):

        """Calcula los impuestos que se deben pagar por este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)

        return self.ventas.all().aggregate(tax=Sum('tax'))['tax']

    def descuento(self):

        """Calcula el descuento que se debe restar a este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)
        return self.ventas.all().aggregate(discount=Sum('discount'))['discount']

    def conceptos(self):

        return ', '.join(
            v.item.descripcion for v in Venta.objects.filter(recibo=self).all())

    def comision_doctor(self):

        return self.total() * Decimal('0.07')

    def comision_radiologo(self):

        return sum(
            v.radiologo() for v in Venta.objects.filter(recibo=self).all())

    def placas(self):

        return sum(v.placas for v in Venta.objects.filter(recibo=self).all())

    def fractional(self):
        """Obtiene la parte decimal del total del :class:`Recibo`"""

        return self.total() % 1

    def integer(self):
        """Obtiene la parte entera del total del :class:`Recibo`"""

        return int(self.total())

    def pagado(self):
        total = Pago.objects.filter(recibo=self).aggregate(
            total=Sum('monto')
        )['total']
        if not total:
            return Decimal()
        return total

    def debido(self):
        return self.total() - self.pagado()

    def save(self, *args, **kwargs):

        if self.pk is None:
            ciudad = self.cajero.profile.ciudad
            ciudad.correlativo_de_recibo = F('correlativo_de_recibo') + 1
            ciudad.save()
            ciudad = Ciudad.objects.get(pk=ciudad.pk)
            self.correlativo = ciudad.correlativo_de_recibo

            turnos = TurnoCaja.objects.filter(usuario=self.cajero,
                                              inicio__lte=self.created).count()
            if turnos == 0:
                turno = TurnoCaja(usuario=self.cajero, inicio=self.created)
                turno.save()

        if self.ciudad is None and self.pk is not None:
            self.ciudad = self.cajero.profile.ciudad

        super(Recibo, self).save(*args, **kwargs)


class Venta(TimeStampedModel):
    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""

    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(blank=True, null=True, max_digits=7,
                                 decimal_places=2)
    impuesto = models.DecimalField(blank=True, default=0, max_digits=7,
                                   decimal_places=2)
    descuento = models.IntegerField(default=0)
    item = models.ForeignKey(ItemTemplate, related_name='ventas',
                             blank=True, null=True)
    recibo = models.ForeignKey(Recibo, related_name='ventas')
    placas = models.IntegerField(default=0)
    descontable = models.BooleanField(default=True)
    discount = models.DecimalField(blank=True, default=0, max_digits=7,
                                   decimal_places=2)
    tax = models.DecimalField(blank=True, default=0, max_digits=7,
                              decimal_places=2)
    total = models.DecimalField(blank=True, default=0, max_digits=11,
                                decimal_places=2)
    monto = models.DecimalField(blank=True, null=True, max_digits=11,
                                decimal_places=2)

    def __unicode__(self):

        return u"{0} a {1}".format(self.item.descripcion, self.recibo.id)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.recibo.id])

    def precio_unitario(self):

        return self.precio

    def precio_previo(self):

        if not self.recibo.tipo_de_venta:
            return self.precio.quantize(dot01)

        aumento = self.recibo.tipo_de_venta.incremento * self.precio
        return (self.precio + aumento).quantize(dot01)

    def discount_calc(self):

        """Calcula la cantidad que se disminuye de la :class:`Venta`"""

        if not self.recibo.tipo_de_venta or not self.descontable:
            return Decimal(0)

        disminucion = self.recibo.tipo_de_venta.disminucion * self.cantidad
        return (self.precio * disminucion).quantize(dot01)

    def radiologo(self):

        """Calcular las comisiones del radiologo que atiende tomando en cuenta
        los descuentos que se han efectuado al recibo"""

        if self.recibo.radiologo is None or self.recibo.radiologo == '':
            return Decimal('0')

        bruto = self.monto * self.item.comision / Decimal("100")
        neto = bruto - bruto * self.descuento / Decimal("100")

        return neto.quantize(dot01)

    def save(self, *args, **kwargs):

        if self.precio is None:
            self.precio = self.item.precio_de_venta

        if not self.recibo.tipo_de_venta or not self.descontable:
            self.discount = Decimal(0)

        disminucion = self.recibo.tipo_de_venta.disminucion * self.cantidad
        self.discount = (self.precio * disminucion).quantize(dot01)

        self.impuesto = self.item.impuestos
        self.monto = self.precio * self.cantidad

        self.tax = Decimal(
            (
                self.precio * self.cantidad - self.discount) *
            self.impuesto).quantize(
            dot01)

        self.total = (
            self.tax + self.precio * self.cantidad - self.discount).quantize(
            dot01)

        super(Venta, self).save(*args, **kwargs)


class Pago(TimeStampedModel):
    """Permite especificar los montos de acuerdo al :class:`TipoPago` utilizado
    por el cliente para pagar el :class:`Recibo`"""

    tipo = ForeignKey(TipoPago, related_name='pagos')
    recibo = ForeignKey(Recibo, related_name='pagos')
    status = models.ForeignKey(StatusPago, blank=True, null=True,
                               related_name='pagos')
    monto = models.DecimalField(blank=True, null=True, max_digits=7,
                                decimal_places=2)
    comprobante = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "Pago en {2} de {0} al recibo {1} {3}".format(self.monto,
                                                             self.recibo.id,
                                                             self.tipo.nombre,
                                                             self.created)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.recibo.id])

    def save(self, *args, **kwargs):
        if self.tipo == TipoPago.objects.get(
                pk=config.PAYMENT_TYPE_PENDING) and self.pk is None:
            self.status = StatusPago.objects.get(
                pk=config.PAYMENT_STATUS_PENDING)

        super(Pago, self).save(*args, **kwargs)


class TurnoCaja(TimeStampedModel):
    usuario = models.ForeignKey(User, related_name='turno_caja')
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    apertura = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    finalizado = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Turno de {0}".format(self.usuario.get_full_name())

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-turno', args=[self.id])

    def recibos(self):

        fin = self.fin
        if fin is None:
            fin = timezone.now()

        return Recibo.objects.filter(cajero=self.usuario,
                                     created__range=(self.inicio, fin)).all()

    def depositos(self):

        fin = self.fin
        if fin is None:
            fin = timezone.now()

        return Deposito.objects.filter(
            created__range=(self.inicio, fin)).all()

    def venta(self):

        return sum(r.total() for r in self.recibos())

    def depositado(self):

        return sum(d.monto for d in self.depositos())

    def ingresos(self):
        return sum(r.pagado() for r in self.recibos())

    def pagos(self):

        metodos = defaultdict(Decimal)
        for tipo in TipoPago.objects.all():
            metodos[tipo] = 0

        for recibo in self.recibos():

            for pago in recibo.pagos.all():
                metodos[pago.tipo] += pago.monto

        return metodos.iteritems()

    def total_cierres(self):

        return sum(
            c.monto for c in CierreTurno.objects.filter(turno=self).all())

    def diferencia(self):

        metodos = defaultdict(Decimal)
        for recibo in self.recibos():

            for pago in recibo.pagos.all():
                metodos[pago.tipo] += pago.monto

        cierres = defaultdict(Decimal)
        for cierre in CierreTurno.objects.filter(turno=self).all():
            cierres[cierre.pago] += cierre.monto

        diferencia = defaultdict(Decimal)
        for tipo in TipoPago.objects.all():
            diferencia[tipo] = cierres[tipo] - metodos[tipo]

        return diferencia.iteritems()

    def diferencia_total(self):

        cierre = sum(
            c.monto for c in CierreTurno.objects.filter(turno=self).all())
        pagos = sum(r.pagado() for r in self.recibos())

        return cierre - pagos - self.apertura


class CierreTurno(TimeStampedModel):
    turno = models.ForeignKey(TurnoCaja, related_name='cierres')
    pago = models.ForeignKey(TipoPago, related_name='cierres')
    monto = models.DecimalField(blank=True, null=True, max_digits=7,
                                decimal_places=2)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.turno.get_absolute_url()


def consolidate_invoice(persona, clone):
    [move_invoice(persona, recibo) for recibo in clone.recibos.all()]


def move_invoice(persona, recibo):
    recibo.paciente = persona
    recibo.save()


persona_consolidation_functions.append(consolidate_invoice)
