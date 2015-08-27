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
from django.db.models.functions import Coalesce

from django.utils import timezone

from django.utils.encoding import python_2_unicode_compatible

from django_extensions.db.models import TimeStampedModel

from django.db.models import F, Sum, Min

from clinique.models import Consulta
from persona.fields import ColorField
from persona.models import Persona, persona_consolidation_functions, \
    transfer_object_to_persona
from inventory.models import ItemTemplate, TipoVenta
from spital.models import Deposito
from users.models import Ciudad

dot01 = Decimal("0.01")


@python_2_unicode_compatible
class TipoPago(TimeStampedModel):
    """
    Define las formas de :class:`Pago` disponibles para ingresar en los
    :class:`Recibo`

    nombre: El nombre que se utilizará en los formularios y etiquetas.
    color: El color que se utilizará para diferenciar en las gráficas.
    solo_asegurados: El :class:`TipoPago` solo estará disponible a las
                     :class:`Persona` que cuenten con un :class:`Contrato`
                     vigente.
    reembolso: Indica si el tipo de pago debe excluirse de los ingresos
               inmediatos al momento de efectuar los calculos de ingresos
    """
    nombre = models.CharField(max_length=255, blank=True, null=True)
    color = ColorField(default='')
    solo_asegurados = models.BooleanField(default=False)
    reembolso = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class StatusPago(TimeStampedModel):
    nombre = models.CharField(max_length=255, blank=True)
    reportable = models.BooleanField(default=True)
    next_status = models.ForeignKey('self', null=True)
    previous_status = models.ForeignKey('self', null=True,
                                        related_name='previous')

    def __str__(self):
        return self.nombre

    def total(self):
        total = Pago.objects.filter(status=self).aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return total


@python_2_unicode_compatible
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

        total = self.ventas.aggregate(
            total=Coalesce(Sum('total'), Decimal())
        )['total']

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

    def __str__(self):

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
            if self.cajero.profile is not None and self.cajero.profile.ciudad \
                    is not None:
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


@python_2_unicode_compatible
class Venta(TimeStampedModel):
    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""

    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(blank=True, null=True, max_digits=11,
                                 decimal_places=2)
    impuesto = models.DecimalField(blank=True, default=0, max_digits=11,
                                   decimal_places=2)
    descuento = models.IntegerField(default=0)
    item = models.ForeignKey(ItemTemplate, related_name='ventas',
                             blank=True, null=True)
    recibo = models.ForeignKey(Recibo, related_name='ventas')
    descontable = models.BooleanField(default=True)
    discount = models.DecimalField(blank=True, default=0, max_digits=11,
                                   decimal_places=2)
    tax = models.DecimalField(blank=True, default=0, max_digits=11,
                              decimal_places=2)
    total = models.DecimalField(blank=True, default=0, max_digits=11,
                                decimal_places=2)
    monto = models.DecimalField(blank=True, null=True, max_digits=11,
                                decimal_places=2)

    def __str__(self):

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


@python_2_unicode_compatible
class Pago(TimeStampedModel):
    """Permite especificar los montos de acuerdo al :class:`TipoPago` utilizado
    por el cliente para pagar el :class:`Recibo`"""

    tipo = ForeignKey(TipoPago, related_name='pagos')
    recibo = ForeignKey(Recibo, related_name='pagos')
    status = models.ForeignKey(StatusPago, blank=True, null=True,
                               related_name='pagos')
    monto = models.DecimalField(default=Decimal(), max_digits=11,
                                decimal_places=2)
    comprobante = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
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


@python_2_unicode_compatible
class TurnoCaja(TimeStampedModel):
    """Allows tracking the :class:`Invoice`s created by a :class:`User` and
    to handle the amounts payed by clients"""

    usuario = models.ForeignKey(User, related_name='turno_caja')
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    apertura = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
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

    def nulos(self):

        return self.recibos().filter(nulo=True).all()

    def depositos(self):

        fin = self.fin
        if fin is None:
            fin = timezone.now()

        return Deposito.objects.filter(
            created__range=(self.inicio, fin)).all()

    def venta(self):

        total = Venta.objects.filter(recibo__in=self.recibos()).aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return total

    def depositado(self):

        return sum(d.monto for d in self.depositos())

    def ingresos(self):

        pagos = Pago.objects.filter(recibo__in=self.recibos()).aggregate(
            total=Sum('monto')
        )['total']

        if pagos is None:
            pagos = Decimal()

        return pagos

    def pagos(self):

        pagos = Pago.objects.filter(recibo__in=self.recibos())

        metodos = defaultdict(Decimal)
        for tipo in TipoPago.objects.all():
            metodos[tipo] = 0

        for pago in pagos.all():
            if pago.monto is None:
                pago.monto = Decimal()
                pago.save()
            metodos[pago.tipo] += pago.monto

        return metodos.iteritems()

    def total_cierres(self):
        total = CierreTurno.objects.filter(turno=self).aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return total

    def diferencia(self):
        """Muestra la diferencia que existe entre los :class:`Pago` que se han
        efectuado a los :class:`Recibo` y los :class:`CierreTurno` que se
        ingresaron al :class:`TurnoCaja` clasificandolos por :class:`TipoPago`
        """

        metodos = defaultdict(Decimal)
        pagos = Pago.objects.filter(recibo__in=self.recibos())

        for pago in pagos.all():
            metodos[pago.tipo] += pago.monto

        cierres = defaultdict(Decimal)
        for cierre in CierreTurno.objects.filter(turno=self).all():
            if cierre.monto is None:
                continue
            cierres[cierre.pago] += cierre.monto

        diferencia = defaultdict(Decimal)
        for tipo in TipoPago.objects.all():
            diferencia[tipo] = cierres[tipo] - metodos[tipo]

        return diferencia.iteritems()

    def diferencia_total(self):

        cierre = self.total_cierres()
        pagos = self.ingresos()

        return cierre - pagos - self.apertura


class CierreTurno(TimeStampedModel):
    turno = models.ForeignKey(TurnoCaja, related_name='cierres')
    pago = models.ForeignKey(TipoPago, related_name='cierres')
    monto = models.DecimalField(blank=True, null=True, max_digits=11,
                                decimal_places=2)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.turno.get_absolute_url()


@python_2_unicode_compatible
class CuentaPorCobrar(TimeStampedModel):
    """Represents all the pending :class:`Pago` que deben recolectarse como un
    grupo"""
    descripcion = models.TextField()
    status = models.ForeignKey(StatusPago)
    minimum = models.DateTimeField(default=timezone.now)
    inicial = models.DecimalField(default=0, max_digits=11, decimal_places=2)

    def __str__(self):

        return self.descripcion

    def monto(self):

        return self.payments().aggregate(
            total=Coalesce(Sum('monto'), Decimal()))['total']

    def pagado(self):

        return self.pagocuenta_set.aggregate(
            total=Coalesce(Sum('monto'), Decimal()))['total']

    def get_absolute_url(self):

        return reverse('invoice-cpc', args=[self.id])

    def payments(self):

        payments = Pago.objects.filter(
            created__range=(self.minimum, self.created),
            status=self.status)
        return payments

    def next_status(self):
        payments = self.payments()

        payments.update(status=self.status.next_status)
        self.status = self.status.next_status
        self.save()

    def previous_status(self):

        payments = self.payments()

        payments.update(status=self.status.previous_status)
        self.status = self.status.previous_status
        self.save()

    def save(self, *args, **kwargs):

        if self.pk is None:

            pending = StatusPago.objects.get(pk=config.PAYMENT_STATUS_PENDING)
            payments = Pago.objects.filter(status=pending)
            self.minimum = payments.aggregate(
                minimum=Min('created')
            )['minimum']

            if self.minimum is None:
                self.minimum = timezone.now()

            self.inicial = self.monto()
            payments.update(status=pending.next_status)
            self.status = pending.next_status

        super(CuentaPorCobrar, self).save(*args, **kwargs)


class PagoCuenta(TimeStampedModel):
    """Describes the payments made to a :class:`Cuenta`"""
    cuenta = models.ForeignKey(CuentaPorCobrar)
    monto = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField()

    def get_absolute_url(self):
        return self.cuenta.get_absolute_url()


class Notification(TimeStampedModel):
    recibo = models.ForeignKey(Recibo)
    completada = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('notification', args=[self.id])

    def consulta(self):
        consulta = Consulta.objects.filter(
            persona=self.recibo.cliente,
            created__lte=self.recibo.created).last()

        return consulta


@python_2_unicode_compatible
class Cotizacion(TimeStampedModel):
    """Permite registrar pagos por productos y servicios"""

    class Meta:
        permissions = (
            ('cajero', 'Permite al usuario gestionar caja'),
        )

    persoa = models.ForeignKey(Persona)
    tipo_de_venta = models.ForeignKey(TipoVenta)
    usuario = models.ForeignKey(User)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True)
    discount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    facturada = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.id])

    def __str__(self):
        """Crea una representación en texto del :class:`Cotizacion`"""

        return self.persona.nombre_completo()

    def total(self):
        total = self.cotizado_set.aggregate(
            total=Coalesce(Sum('total'), Decimal())
        )['total']

        return total

    def subtotal(self):
        """Calcula el monto antes de impuestos"""

        return \
            self.ventas.aggregate(
                total=Sum('monto', output_field=models.DecimalField()))['total']

    def impuesto(self):
        """Calcula los impuestos que se deben pagar por este :class:`Cotizacion`
        """

        return self.ventas.all().aggregate(tax=Sum('tax'))['tax']

    def descuento(self):
        """Calcula el descuento que se debe restar a este :class:`Cotizacion`"""
        return self.ventas.all().aggregate(discount=Sum('discount'))['discount']

    def conceptos(self):
        return ', '.join(
            v.item.descripcion for v in
            Cotizado.objects.filter(recibo=self).all())

    def save(self, *args, **kwargs):
        if self.ciudad is None:
            self.ciudad = self.usuario.profile.ciudad

        super(Cotizacion, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Cotizado(TimeStampedModel):
    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""
    cotizacion = models.ForeignKey(Cotizacion)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    porcentaje_descuento = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    descontable = models.BooleanField(default=True)

    def __str__(self):

        return u"{0} a {1}".format(self.item.descripcion, self.recibo.id)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.recibo.id])

    def save(self, *args, **kwargs):

        if self.precio is None:
            self.precio = self.item.precio_de_venta

        if not self.cotizacion.tipo_de_venta or not self.descontable:
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

        super(Cotizado, self).save(*args, **kwargs)


def consolidate_invoice(persona, clone):
    """Transfers all :class:`Recibo` from a duplicate :class:`Persona` to the
    original one"""
    [move_invoice(persona, recibo) for recibo in clone.recibos.all()]


def move_invoice(persona, recibo):
    """Transfers a single :class:`Recibo` to a :class:`Persona`"""
    recibo.cliente = persona
    recibo.save()


def consolidate_cotizacion(persona, clone):
    """
    Transfers all :class:`Cotizacion` from a duplicate :class:`Persona` to the
    original one
    """
    [transfer_object_to_persona(cotizacion, persona) for cotizacion in
     clone.cotizacion_set.all()]


persona_consolidation_functions.append(consolidate_invoice)
persona_consolidation_functions.append(consolidate_cotizacion)
