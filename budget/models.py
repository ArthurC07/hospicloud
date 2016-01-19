# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2015 Carlos Flores <cafg10@gmail.com>
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

from copy import deepcopy
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from contracts.models import Aseguradora
from hospinet.utils import get_current_month_range, get_previous_month_range
from inventory.models import Proveedor
from invoice.models import Venta, Pago, PagoCuenta
from persona.models import Persona
from users.models import Ciudad


def ingreso_global_periodo(inicio, fin):
    return Venta.objects.select_related('recibo', 'recibo__ciudad').filter(
            recibo__cliente__ciudad__tiene_presupuesto_global=True,
            recibo__created__range=(inicio, fin),
            recibo__nulo=False
    ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']


@python_2_unicode_compatible
class Presupuesto(TimeStampedModel):
    """Define un presupuesto financiero para una :class:`Ciudad` específica,
    permitiendo calcular lo gastado y lo que aún no ha sido pagado"""
    ciudad = models.ForeignKey(Ciudad)
    activo = models.BooleanField(default=True)
    porcentaje_global = models.DecimalField(max_digits=3, decimal_places=2,
                                            default=Decimal)
    inversion = models.BooleanField(default=False)

    def __str__(self):
        return _('Presupuesto de {0}').format(self.ciudad.nombre)

    def get_absolute_url(self):
        """
        :return: The absolute url for each instance of this model
        """
        return reverse('budget', args=[self.id])

    def total_presupuestado(self):
        return Cuenta.objects.filter(
                presupuesto=self
        ).aggregate(
                total=Coalesce(Sum('limite'), Decimal())
        )['total']

    def gastos_por_periodo(self, inicio, fin):
        return Gasto.objects.filter(fecha_de_pago__range=(inicio, fin),
                                    cuenta__in=self.cuenta_set.all(),
                                    ejecutado=True)

    def total_gastos_por_periodo(self, inicio, fin):
        return self.gastos_por_periodo(inicio, fin).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def gastos_mes_actual(self):
        fin, inicio = get_current_month_range()

        return self.gastos_por_periodo(inicio, fin)

    def total_gastos_mes_actual(self):
        return self.gastos_mes_actual().aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def porcentaje_ejecutado_mes_actual(self):
        return self.total_gastos_mes_actual() / max(self.total_presupuestado(),
                                                    1) * 100

    def ingresos_mes_actual(self):
        fin, inicio = get_current_month_range()

        return self.ingresos_periodo(fin, inicio)

    def ingreso_global_mes_anterior(self):
        fin, inicio = get_previous_month_range()
        return ingreso_global_periodo(inicio, fin) * self.porcentaje_global

    def ingresos_mes_anterior(self):
        return self.ingresos_mes_locales_anterior() + \
               self.ingreso_global_mes_anterior()

    def ingresos_mes_locales_anterior(self):
        fin, inicio = get_previous_month_range()

        return self.ingresos_periodo(fin, inicio)

    def ingresos_periodo(self, fin, inicio):
        condition = Q(
                recibo__cliente__ciudad__tiene_presupuesto_global=False) | Q(
                recibo__cliente__ciudad__isnull=True)

        return Venta.objects.select_related('recibo__ciudad',
                                            'recibo__cliente__ciudad').filter(
                condition,
                recibo__created__range=(inicio, fin),
                recibo__ciudad=self.ciudad,
                recibo__nulo=False
        ).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def get_equilibiio(self):
        return self.ingresos_mes_anterior() - self.total_gastos_mes_actual()

    def porcentaje_consumido(self):
        gastos = self.total_gastos_mes_actual()
        ingresos = self.ingresos_mes_actual()

        return gastos / max(ingresos, 1) * 100


@python_2_unicode_compatible
class Cuenta(TimeStampedModel):
    """
    Define una agrupación de :class:`Gasto`s referentes a un rubro
    determinado. Estos :class:`Gasto` representan lo ejecutado y las cuentas
    por pagar
    """

    class Meta:
        ordering = ('nombre',)

    presupuesto = models.ForeignKey(Presupuesto)
    nombre = models.CharField(max_length=255)
    limite = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return _('{0} en {1}').format(self.nombre,
                                      self.presupuesto.ciudad.nombre)

    def get_absolute_url(self):
        """
        :return: The absolute url for each instance of this model
        """
        return reverse('budget-control', args=[self.presupuesto.id])

    def cuentas_por_pagar(self):
        """Obtiene los :class:`Gasto`s que aún no han sido ejectuados y por lo
        tanto son cuentas por pagar"""

        return Gasto.objects.filter(cuenta=self, ejecutado=False)

    def gastos_por_periodo(self, inicio, fin):
        """obtiene los :class:`Gasto`s que ya fueron ejecutados y que han sido
        descargado del flujo de dinero de la empresa"""
        return Gasto.objects.filter(cuenta=self, ejecutado=True,
                                    fecha_de_pago__range=(inicio, fin))

    def total_gastos_por_periodo(self, inicio, fin):
        """Obtiene el tal de :class:`Gasto`s de la :class:`Cuenta` en un periodo
        determinado de tiempo"""

        return self.gastos_por_periodo(inicio, fin).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def gastos_mes_actual(self):
        """Obtiene los :class:`Gasto` del mes actual"""

        fin, inicio = get_current_month_range()

        return self.gastos_por_periodo(inicio, fin)

    def total_gastos_mes_actual(self):
        """
        Calculates the sum of :class:`Gasto` during the current month
        :return: The sum of all :class:`Gasto`s monto from the current month
        """
        return self.gastos_mes_actual().aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def total_cuentas_por_pagar(self):
        """
        Calculates the total of unpayed :class:`Gasto` that have been charged
        to the :class:`Presupuesto`
        :return: The sum of unpayed :class:`Gasto`'s monto
        """
        return self.cuentas_por_pagar().aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def porcentaje_ejecutado_mes_actual(self):
        return self.total_gastos_mes_actual() / max(self.limite, 1) * 100


@python_2_unicode_compatible
class Fuente(TimeStampedModel):
    """
    Explains where the money for :class:`Gasto`s is comming from.
    """

    class Meta:
        ordering = ('nombre',)

    nombre = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    caja = models.BooleanField(default=False)

    def __str__(self):
        """
        :return: String representation of the current model
        """
        return self.nombre


@python_2_unicode_compatible
class Gasto(TimeStampedModel):
    """Representa las transacciones monetarias realizadas por el personal de la
    :class:`Ciudad` y que son restadas del :class:`Presupuesto` vigente

    Cuando un :class:`Gasto` aún no está ejectuado, se encuentra en cuentas por
    pagar y puede mantenerse en espera hasta us fecha máxima de pago, reflejada
    por el campo correspondiente.
    """
    cuenta = models.ForeignKey(Cuenta, verbose_name=_('Tipo de Cargo'))
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    fecha_en_factura = models.DateTimeField(default=timezone.now)
    numero_de_factura = models.CharField(max_length=255, default='')
    fecha_maxima_de_pago = models.DateTimeField(default=timezone.now)
    factura = models.FileField(upload_to='budget/gasto/%Y/%m/%d',
                               blank=True, null=True)
    fuente_de_pago = models.ForeignKey(Fuente, null=True, blank=True)
    numero_de_comprobante_de_pago = models.CharField(max_length=255, blank=True,
                                                     null=True)
    comprobante_de_pago = models.FileField(upload_to='budget/gasto/%Y/%m/%d',
                                           blank=True, null=True)
    fecha_de_pago = models.DateTimeField(default=timezone.now)
    ejecutado = models.BooleanField(default=False)
    numero_pagos = models.IntegerField(default=1)
    recepcion_de_facturas_originales = models.BooleanField(default=False)
    fecha_de_recepcion_de_factura = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __str__(self):
        """
        :return: String representation of the current model
        """
        return self.descripcion

    def get_absolute_url(self):
        """
        :return: The absolute url for each instance of this model
        """
        return reverse('budget-control', args=[self.cuenta.presupuesto.id])

    def ejecutar(self):
        """
        Registra el pago del :class:`Gasto` actual
        """
        self.ejecutado = True
        self.fuente_de_pago.monto -= self.monto
        self.fuente_de_pago.save()
        self.save()

    def clonar(self):
        """
        Crea una copia identica del :class:`Gasto` actual pero que aun no ha
        sido guardada en la BD.
        :return: Replica del :class:`Gasto` actual sin guardar.
        """
        gasto = deepcopy(self)
        gasto.id = None

        return gasto

    def schedule(self):

        if self.numero_pagos <= 1:
            return

        for n in range(self.numero_pagos - 1):
            gasto = self.clonar()
            delta = relativedelta(months=+n)
            gasto.numero_pagos = 1
            gasto.fecha_maxima_de_pago = gasto.fecha_maxima_de_pago + delta

            gasto.save()

        self.numero_pagos = 1
        self.save()

    def pago_parcial(self, monto):
        """
        Crea un pago parcial para el :class:`Gasto` y lo aplica dividiendo el
        gasto en dos segun la cantidad especificada.
        :param monto: Valor monetario del pago a ingresar
        """
        gasto = self.clonar()
        gasto.monto = monto
        gasto.save()

        self.monto -= monto
        self.save()


class Income(TimeStampedModel):
    """
    Describe los ingresos particulares
    """
    ciudad = models.ForeignKey(Ciudad)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    def get_absolute_url(self):
        """
        :return: The absolute url for each instance of this model
        """
        return reverse('budget-income', args=[self.id])

    def facturado_periodo(self, inicio, fin):
        condition = Q(
                recibo__cliente__ciudad__tiene_presupuesto_global=False) | Q(
                recibo__cliente__ciudad__isnull=True)

        return Pago.objects.filter(
                condition,
                recibo__created__range=(inicio, fin),
                recibo__nulo=False,
                recibo__ciudad=self.ciudad
        ).values('tipo__nombre').annotate(
                total=Coalesce(Sum('monto'), Decimal())).order_by()

    def facturado_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.facturado_periodo(inicio, fin)

    def pagos_periodo(self, inicio, fin):
        return Pago.objects.filter(
                tipo__reembolso=False,
                recibo__ciudad=self.ciudad,
                recibo__created__range=(inicio, fin),
                recibo__nulo=False
        ).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def pagos_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.pagos_periodo(inicio, fin)

    def ingresado_periodo(self, inicio, fin):
        return self.pagos_periodo(inicio, fin)

    def ingresado_mes_actual(self):
        return self.pagos_mes_actual()

    def reembolsos_periodo(self, inicio, fin):
        return PagoCuenta.objects.filter(
                fecha__range=(inicio, fin)
        )

    def total_reembolsos_periodo(self, inicio, fin):
        return self.reembolsos_periodo(inicio, fin).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def reembolsos_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.reembolsos_periodo(inicio, fin)

    def total_reembolsos_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.total_reembolsos_periodo(inicio, fin)

    def pagos_reembolsados_periodo(self, inicio, fin):
        return Pago.objects.filter(
                tipo__reembolso=True,
                recibo__ciudad=self.ciudad,
                status__reportable=False,
                modified__range=(inicio, fin),
                recibo__nulo=False
        )

    def total_pagos_reembolsados_periodo(self, inicio, fin):
        return self.pagos_reembolsados_periodo(inicio, fin).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def pagos_reembolsados_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.pagos_reembolsados_periodo(inicio, fin)

    def total_pagos_reembolsados_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.total_pagos_reembolsados_periodo(inicio, fin)

    def pagos_por_reembolsar_periodo(self, inicio, fin):
        return Pago.objects.filter(
                tipo__reembolso=True,
                recibo__ciudad=self.ciudad,
                status__reportable=True,
                modified__range=(inicio, fin),
                recibo__nulo=False
        )

    def total_pago_por_reembolsar_periodo(self, inicio, fin):
        return self.pagos_por_reembolsar_periodo(inicio, fin).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

    def total_pago_por_reembolsar_mes_actual(self):
        fin, inicio = get_current_month_range()
        return self.total_pago_por_reembolsar_periodo(inicio, fin)

    def pendiente_aseguradoras(self):
        fin, inicio = get_current_month_range()

        return [
            (aseguradora,
             Pago.objects.filter(
                     tipo__reembolso=True,
                     recibo__ciudad=self.ciudad,
                     recibo__created__range=(inicio, fin),
                     recibo__nulo=False,
                     recibo__cliente__in=Persona.objects.filter(
                             contratos__master__aseguradora=aseguradora)
             ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total'],
             Pago.objects.filter(
                     tipo__reembolso=True,
                     recibo__ciudad=self.ciudad,
                     status__reportable=False,
                     modified__range=(inicio, fin),
                     recibo__nulo=False,
                     recibo__cliente__in=Persona.objects.filter(
                             contratos__master__aseguradora=aseguradora)
             ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total'],
             Pago.objects.filter(
                     tipo__reembolso=True,
                     status__reportable=True,
                     recibo__ciudad=self.ciudad,
                     recibo__nulo=False,
                     recibo__cliente__in=Persona.objects.filter(
                             contratos__master__aseguradora=aseguradora)
             ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total'])
            for aseguradora in Aseguradora.objects.all()
            ]


@python_2_unicode_compatible
class PresupuestoMes(TimeStampedModel):
    """
    Describe el monto mensual de un presupuesto asignado a una :class:`Cuenta`
    """
    cuenta = models.ForeignKey(Cuenta)
    mes = models.IntegerField()
    anio = models.IntegerField(verbose_name=_('Año'))
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    procesado = models.BooleanField(default=False)
    completar_anio = models.BooleanField(default=False,
                                         verbose_name=_('Completar Año'))

    def get_absolute_url(self):
        """
        :return: The absolute url for each instance of this model
        """
        return reverse('monthly-budget', args=[self.id])

    def __str__(self):
        """
        :return: String representation of the current model
        """
        return _('Presupuesto de {0} para {1} de {2} en {3}').format(
                self.cuenta.nombre,
                self.mes,
                self.anio,
                self.cuenta.presupuesto.ciudad.nombre
        )

    def save(self, **kwargs):
        """
        Saves the :class:`PresupuestoMes` and replicates it if needed
        :param kwargs:
        :return:
        """
        if not self.procesado and self.completar_anio:
            for n in range(1, 13):
                if n == self.mes:
                    continue
                presupuesto = PresupuestoMes()
                presupuesto.cuenta = self.cuenta
                presupuesto.monto = self.monto
                presupuesto.mes = n
                presupuesto.anio = self.anio
                presupuesto.procesado = True
                presupuesto.save()
            self.procesado = True

        super(PresupuestoMes, self).save(**kwargs)
