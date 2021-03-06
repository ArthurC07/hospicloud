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
from __future__ import unicode_literals

from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Sum, Min, QuerySet
from django.db.models.fields.related import ForeignKey
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from clinique.models import Consulta
from contracts.models import Aseguradora
from inventory.models import ItemTemplate, TipoVenta, Proveedor
from invoice import managers
from persona.fields import ColorField
from persona.models import Persona, persona_consolidation_functions, \
    transfer_object_to_persona
from spital.models import Deposito
from users.models import Ciudad, LegalData

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
    mensual = models.BooleanField(default=False)
    reportable = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class StatusPago(TimeStampedModel):
    nombre = models.CharField(max_length=255, blank=True)
    reportable = models.BooleanField(default=True)
    next_status = models.ForeignKey('self', null=True)
    previous_status = models.ForeignKey('self', null=True,
                                        related_name='previous')
    pending = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def total(self):
        return Pago.objects.filter(status=self).aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']


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
    legal_data = models.ForeignKey(LegalData, blank=True, null=True)
    cajero = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               related_name='recibos')
    tipo_de_venta = models.ForeignKey(TipoVenta, blank=True, null=True)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    correlativo = models.IntegerField(default=0)
    credito = models.BooleanField(default=False)
    cerrado = models.BooleanField(default=False)
    nulo = models.BooleanField(default=False)
    emision = models.DateTimeField(default=timezone.now)
    month_offset = models.IntegerField(default=0)

    objects = managers.ReciboManager()

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.id])

    def vencimiento(self):

        return self.emision + timedelta(days=self.ciudad.company.receipt_days)

    def facturacion(self):

        return self.created - relativedelta(months=1 + self.month_offset)

    def total(self):

        if self.nulo:
            return Decimal()

        return self.ventas.aggregate(
            total=Coalesce(Sum('total'), Decimal())
        )['total']

    @property
    def numero(self):
        """
        Crea el número segun los requerimientos de la DEI, permitiendo de este
        modo tener múltiples lugares que emitan recibos y que tengan diferentes
        prefijos para sus recibos.
        :return:
        """
        legal_data = self.legal_data
        if legal_data is None:
            if self.cajero is None or self.cajero.profile is None or \
                            self.cajero.profile.ciudad is None:
                return self.correlativo

            legal_data = self.cajero.profile.ciudad.recibo

        return '{0}-{1:08d}'.format(legal_data.prefijo, self.correlativo)

    def other_currency(self):

        return (
            self.total() / self.ciudad.company.cambio_monetario
        ).quantize(dot01)

    def impuesto_other(self):

        return (
            self.impuesto() / self.ciudad.company.cambio_monetario
        ).quantize(dot01)

    def descuento_other(self):

        return (
            self.descuento() / self.ciudad.company.cambio_monetario
        ).quantize(dot01)

    def subtotal_other(self):

        return (
            self.subtotal() / self.ciudad.company.cambio_monetario
        ).quantize(dot01)

    def anular(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""

        self.nulo = True

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
            return _('{0} **NULO**').format(self.cliente.nombre_completo())

        return self.cliente.nombre_completo()

    def subtotal(self):

        """Calcula el monto antes de impuestos"""

        if self.nulo:
            return Decimal()

        return self.ventas.aggregate(
            total=Coalesce(Sum('monto', output_field=models.DecimalField()),
                           Decimal())
        )['total']

    def impuesto(self):

        """Calcula los impuestos que se deben pagar por este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)

        return self.ventas.all().aggregate(
            tax=Coalesce(Sum('tax'), Decimal())
        )['tax']

    def descuento(self):

        """Calcula el descuento que se debe restar a este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)
        return self.ventas.all().aggregate(
            discount=Coalesce(Sum('discount'), Decimal())
        )['discount']

    def conceptos(self):

        return ', '.join(
            v.item.descripcion for v in
            Venta.objects.filter(recibo=self).all())

    def fractional(self):
        """Obtiene la parte decimal del total del :class:`Recibo`"""

        return self.total() % 1

    def integer(self):
        """Obtiene la parte entera del total del :class:`Recibo`"""

        return int(self.total())

    def pagado(self):

        return self.pagos.aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def debido(self):
        return self.total() - self.pagado()

    def save(self, **kwargs):

        """
        Guarda el recibo asignando :class:`Ciudad` y luego generando el
        correlativo correspondiente a la ciudad
        """

        if self.pk is None:
            if self.cajero.profile is not None \
                    and self.cajero.profile.ciudad is not None \
                    and self.cajero.profile.ciudad.recibo is not None:
                self.asignar_correlativo()

            turnos = TurnoCaja.objects.filter(
                usuario=self.cajero,
                inicio__lte=timezone.now()
            ).count()

            if turnos == 0:
                turno = TurnoCaja(usuario=self.cajero, inicio=timezone.now())
                turno.save()

        self.asignar_ciudad()

        super(Recibo, self).save(**kwargs)

    def asignar_ciudad(self):
        """
        Assigns the :class:`Ciudad` and :class:`LegalData` to the
        :class:`Recibo`
        """
        if self.ciudad is None:
            self.ciudad = self.cajero.profile.ciudad
        self.legal_data = self.ciudad.recibo

    def asignar_correlativo(self):
        """
        Crea el correlativo del recibo correspondiente a la :class:`Ciudad` que
        emite el recibo, esto sirve para crear el número según los
        requerimientos de la DEI
        :return:
        """

        cai = self.cajero.profile.ciudad.recibo
        cai.correlativo = F('correlativo') + 1
        cai.save()
        cai.refresh_from_db()
        self.correlativo = cai.correlativo


@python_2_unicode_compatible
class Venta(TimeStampedModel):
    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""

    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(blank=True, null=True, max_digits=12,
                                 decimal_places=4)
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

    objects = managers.VentaManager()

    def __str__(self):

        return _("{0} a {1}").format(self.item.descripcion, self.recibo.id)

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

        self.recalculate()

        super(Venta, self).save(*args, **kwargs)

    def recalculate(self):
        """
        Calculates values for the different monetary values implicit in each
        sale.
        :return:
        """
        if self.precio is None:
            self.precio = self.item.precio_de_venta
        if not self.recibo.tipo_de_venta or not self.descontable:
            self.discount = Decimal(0)
        disminucion = self.recibo.tipo_de_venta.disminucion * self.cantidad
        self.discount = (self.precio * disminucion).quantize(dot01)
        self.impuesto = self.item.impuestos
        self.monto = self.precio * self.cantidad
        self.tax = Decimal((self.precio * self.cantidad - self.discount) *
                           self.impuesto).quantize(dot01)
        self.total = (
            self.tax + self.precio * self.cantidad - self.discount
        ).quantize(dot01)


class PagoQuerySet(models.QuerySet):
    """
    Provides shortcuts to obtain common used data
    """

    def cuentas_por_cobrar(self):
        """
        Obtains all the :class:`Pago` that are yet to be completed or that
        represent a partial payment of the :class:`Invoice`
        """
        return self.filter(
            completado=False,
            tipo__reportable=True,
        )

    def mensual(self):
        """
        Obtains all :class:`Pago` clasified as monthly
        """
        return self.filter(tipo__mensual=True)

    def reembolso(self):
        """
        Obtains all :class:`Pago` classified as reimbursement
        """
        return self.filter(tipo__reembolso=True)

    def diarias(self):
        """
        Obtains all :class:`Pago` that are payed inmediatly
        """
        return self.exclude(tipo__mensual=True).exclude(tipo__reembolso=True)


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
    aseguradora = models.ForeignKey(Aseguradora, blank=True, null=True)
    completado = models.BooleanField(default=False)

    objects = PagoQuerySet.as_manager()

    def __str__(self):
        return _("Pago en {2} de {0} al recibo {1} {3}").format(
            self.monto,
            self.recibo.id,
            self.tipo.nombre,
            self.created
        )

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.recibo.get_absolute_url()

    def obtener_consolidacion_faltante(self):
        """
        :return: Amount missing from payment
        """
        total = self.detallepago_set.aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return self.monto - total

    def save(self, **kwargs):
        if self.tipo.reembolso and self.pk is None:
            self.status = StatusPago.objects.filter(pending=True).first()

        super(Pago, self).save(**kwargs)


@python_2_unicode_compatible
class TurnoCaja(TimeStampedModel):
    """Allows tracking the :class:`Invoice`s created by a :class:`User` and
    to handle the amounts payed by clients"""

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='turno_caja')
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    apertura = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return _("Turno de {0}").format(self.usuario.get_full_name())

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-turno', args=[self.id])

    def recibos(self):

        fin = self.fin
        if fin is None:
            fin = timezone.now()

        return Recibo.objects.filter(
            cajero=self.usuario,
            created__range=(self.inicio, fin)
        ).prefetch_related(
            'legal_data',
            'cliente',
        )

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
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return pagos

    def pagos(self):

        return Pago.objects.filter(recibo__in=self.recibos()).order_by().values(
            'tipo__nombre').annotate(
            monto=Sum('monto'),
        )

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

        return list(diferencia.items())

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
    """
    Represents all the pending :class:`Pago` que deben recolectarse como un
    grupo
    """

    class Meta:
        ordering = ('-created',)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    descripcion = models.TextField()
    status = models.ForeignKey(StatusPago)
    minimum = models.DateTimeField(default=timezone.now)
    inicial = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    enviadas = models.IntegerField(default=0)

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
        """
        :return: A query to all the payments registered to a
        :class:`CuentaPorCobrar`
        """
        payments = Pago.objects.filter(
            recibo__created__range=(self.minimum, self.created),
            status=self.status).order_by('recibo__created')
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

            self.status = StatusPago.objects.filter(pending=True).first()
            payments = Pago.objects.filter(status=self.status)
            self.minimum = payments.aggregate(
                minimum=Min('created')
            )['minimum']

            if self.minimum is None:
                self.minimum = timezone.now()

            self.inicial = self.monto()

        super(CuentaPorCobrar, self).save(*args, **kwargs)


class PagoCuenta(TimeStampedModel):
    """Describes the payments made to a :class:`Cuenta`"""
    cuenta = models.ForeignKey(CuentaPorCobrar)
    monto = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField()
    archivo = models.FileField(blank=True, null=True, )

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

    persona = models.ForeignKey(Persona)
    tipo_de_venta = models.ForeignKey(TipoVenta)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True)
    discount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    facturada = models.BooleanField(default=False)
    credito = models.BooleanField(default=False)
    terminada = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('cotizacion', args=[self.id])

    def __str__(self):
        """Crea una representación en texto del :class:`Cotizacion`"""

        return self.persona.nombre_completo()

    def total(self):
        total = self.cotizado_set.aggregate(
            total=Coalesce(Sum('total'), Decimal())
        )['total']

        return total

    def facturar(self):
        recibo = Recibo()
        recibo.cliente = self.persona
        recibo.tipo_de_venta = self.tipo_de_venta
        recibo.cajero = self.usuario
        recibo.ciudad = self.ciudad
        recibo.discount = self.discount
        recibo.credito = self.credito
        recibo.save()

        for cotizado in self.cotizado_set.all():
            venta = Venta()
            venta.recibo = recibo
            venta.item = cotizado.item
            venta.cantidad = cotizado.cantidad
            venta.descripcion = cotizado.descripcion
            venta.porcentaje_descuento = cotizado.porcentaje_descuento
            venta.precio = cotizado.precio
            venta.impuesto = cotizado.impuesto
            venta.discount = cotizado.discount
            venta.tax = cotizado.tax
            venta.total = cotizado.total
            venta.monto = cotizado.monto
            venta.descontable = cotizado.descontable
            venta.save()

        self.facturada = True
        self.save()

        return recibo

    def subtotal(self):
        """Calcula el monto antes de impuestos"""

        return self.cotizado_set.aggregate(
            total=Coalesce(Sum('monto', output_field=models.DecimalField()),
                           Decimal())
        )['total']

    def impuesto(self):
        """Calcula los impuestos que se deben pagar por este :class:`Cotizacion`
        """

        return self.cotizado_set.all().aggregate(
            tax=Coalesce(Sum('tax'), Decimal())
        )['tax']

    def descuento(self):
        """Calcula el descuento que se debe restar a este :class:`Cotizacion`"""
        return self.cotizado_set.all().aggregate(
            discount=Coalesce(Sum('discount'), Decimal())
        )['discount']

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

    class Meta:
        ordering = ('-created',)

    cotizacion = models.ForeignKey(Cotizacion)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True)
    porcentaje_descuento = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=12, decimal_places=4,
                                 null=True, blank=True)
    impuesto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    descontable = models.BooleanField(default=True)

    def __str__(self):

        return _("{0} a {1}").format(self.item.descripcion, self.cotizacion.id)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return self.cotizacion.get_absolute_url()

    def save(self, *args, **kwargs):

        if self.precio is None:
            self.precio = self.item.precio_de_venta

        if not self.cotizacion.tipo_de_venta or not self.descontable:
            self.discount = Decimal(0)

        disminucion = self.cotizacion.tipo_de_venta.disminucion * self.cantidad
        self.discount = (self.precio * disminucion).quantize(dot01)

        self.impuesto = self.item.impuestos
        self.monto = self.precio * self.cantidad

        self.tax = Decimal(
            (self.precio * self.cantidad - self.discount) * self.impuesto
        ).quantize(dot01)

        self.total = (
            self.tax + self.precio * self.cantidad - self.discount).quantize(
            dot01)

        super(Cotizado, self).save(*args, **kwargs)


@python_2_unicode_compatible
class ComprobanteDeduccion(TimeStampedModel):
    """
    Registra las deducciones que se hacen a los :class:`Proveedor`es de acuerdo
    a las leyes del país.
    """
    proveedor = models.ForeignKey(Proveedor, null=True)
    ciudad = models.ForeignKey(Ciudad)
    correlativo = models.IntegerField()
    cai_proveedor = models.CharField(max_length=255, blank=True)
    numero_de_documento = models.CharField(max_length=255, blank=True)
    fecha_de_emision = models.DateTimeField(default=timezone.now)
    legal_data = models.ForeignKey(LegalData, blank=True, null=True)

    def __str__(self):
        if self.proveedor is None:
            return str(self.correlativo)
        return self.proveedor.name

    def get_absolute_url(self):
        return reverse('comprobante', args=[self.id])

    def numero(self):
        return _('{0}-{1}').format(self.legal_data.prefijo, self.correlativo)

    def total(self):
        """
        :return: El total de los :class:`ConceptoDeduccion` que han sido
        ingresados en este comprobante
        """
        return ConceptoDeduccion.objects.filter(comprobante=self).aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.legal_data = self.ciudad.comprobante

            self.legal_data.correlativo = F('correlativo') + 1
            self.legal_data.save()
            self.legal_data.refresh_from_db()
            self.correlativo = self.legal_data.correlativo

        super(ComprobanteDeduccion, self).save(*args, **kwargs)


class ConceptoDeduccion(TimeStampedModel):
    """
    Describe el concepto de una deducción que ha sido sustraida de un pago a
    proveedor
    """
    comprobante = models.ForeignKey(ComprobanteDeduccion)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    concepto = models.ForeignKey(ItemTemplate)
    descripcion = models.TextField(blank=True)

    def get_absolute_url(self):
        return self.comprobante.get_absolute_url()


@python_2_unicode_compatible
class NotaCredito(TimeStampedModel):
    """
    Reflects an legal document used to nullify emited :class:`Recibo`s when
    they have been handled to the :class:`Persona`.

    recibo: :class:`Recibo` that has :class:`Item`s to be nullified
    correlativo: numerical identifier based in the :class:`Ciudad` it is
                 extended
    motivo_de_emision: Specifies the reason the :class:`Recibo` is being
                       modified
    """

    MOTIVOS = (
        ('AN', _('Anulación')),
        ('DV', _('Devolución')),
        ('DE', _('Descuento')),
    )

    recibo = models.ForeignKey(Recibo)
    correlativo = models.IntegerField(default=0)
    motivo_de_emision = models.CharField(max_length=1, choices=MOTIVOS,
                                         blank=True)
    cerrada = models.BooleanField(default=False)
    legal_data = models.ForeignKey(LegalData, blank=True, null=True)

    def numero(self):
        return '{0}-{1:08d}'.format(self.legal_data.prefijo, self.correlativo)

    def __str__(self):
        return str(self.correlativo)

    def save(self, *args, **kwargs):
        """
        Guarda la :class:`NotaCredito` asignando :class:`Ciudad` y luego
        generando el correlativo correspondiente a la ciudad.
        """
        if self.pk is None:
            self.legal_data = self.recibo.ciudad.comprobante

            self.legal_data.correlativo = F('correlativo') + 1
            self.legal_data.save()
            self.legal_data.refresh_from_db()
            self.correlativo = self.legal_data.correlativo

        super(NotaCredito, self).save(*args, **kwargs)


class DetalleCredito(TimeStampedModel):
    """
    Holds the description of an :class:`ItemTemplate` that has been discounted
    or diminished.
    """
    nota = models.ForeignKey(NotaCredito)
    item = models.ForeignKey(ItemTemplate)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=11, decimal_places=2)
    impuesto = models.DecimalField(max_digits=11, decimal_places=2)
    monto_impuesto = models.DecimalField(max_digits=11, decimal_places=2)
    monto = models.DecimalField(max_digits=11, decimal_places=2)

    def save(self, **kwargs):
        self.precio = self.item.precio_de_venta
        self.monto = self.precio * self.cantidad
        self.impuesto = self.item.impuestos
        self.monto_impuesto = self.impuesto * self.monto

        super(DetalleCredito, self).save(**kwargs)


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
