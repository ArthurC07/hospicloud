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
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.models import TimeStampedModel

from inventory.models import Proveedor
from invoice.models import Venta
from users.models import Ciudad, get_current_month_range


@python_2_unicode_compatible
class Presupuesto(TimeStampedModel):
    """Define un presupuesto financiero para una :class:`Ciudad` específica"""
    ciudad = models.ForeignKey(Ciudad)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return u'Presupuesto de {0}'.format(self.ciudad.nombre)

    def get_absolute_url(self):
        return reverse('budget', args=[self.id])

    def total_presupuestado(self):
        return Cuenta.objects.filter(
            presupuesto=self
        ).aggregate(total=Sum('limite'))['total']

    def gastos_por_periodo(self, inicio, fin):
        return Gasto.objects.filter(created__range=(inicio, fin),
                                    cuenta__in=self.cuenta_set.all())

    def total_gastos_por_periodo(self, inicio, fin):
        gasto = self.gastos_por_periodo().aggregate(total=Sum('monto'))['total']

        if gasto is None:
            return Decimal()

        return gasto

    def gastos_mes_actual(self):
        fin, inicio = get_current_month_range()

        return self.gastos_por_periodo(inicio, fin)

    def total_gastos_mes_actual(self):
        gastos = self.gastos_mes_actual().aggregate(total=Sum('monto'))['total']

        if gastos is None:
            return Decimal()

        return gastos

    def porcentaje_ejecutado_mes_actual(self):
        return self.total_gastos_mes_actual() / max(self.total_presupuestado(),
                                                    1) * 100

    def ingresos_mes_actual(self):

        fin, inicio = get_current_month_range()

        ventas = Venta.objects.select_related('recibo').filter(
            recibo__created__range=(inicio, fin),
            recibo__ciudad=self.ciudad
        ).aggregate(total=Sum('monto'))['total']

        if ventas is None:

            ventas = Decimal()

        return ventas

    def porcentaje_consumido(self):

        gastos = self.total_gastos_mes_actual()
        ingresos = self.ingresos_mes_actual()

        return gastos / max(ingresos, 1) * 100


@python_2_unicode_compatible
class Cuenta(TimeStampedModel):
    """Define una agrupación de gastos referentes a un rubro determinado"""
    presupuesto = models.ForeignKey(Presupuesto)
    nombre = models.CharField(max_length=255)
    limite = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):

        return self.nombre

    def get_absolute_url(self):

        return self.presupuesto.get_absolute_url()

    def gastos_por_periodo(self, inicio, fin):

        return Gasto.objects.filter(cuenta=self, created__range=(inicio, fin))

    def total_gastos_por_periodo(self, inicio, fin):

        """Obtiene el tal de :class:`Gasto`s de la :class:`Cuenta` en un periodo
        determinado de tiempo"""

        gastos = self.gastos_por_periodo(inicio, fin).aggregate(
            total=Sum('monto')
        )['total']

        if gastos is None:
            return Decimal()

        return gastos

    def gastos_mes_actual(self):

        fin, inicio = get_current_month_range()

        return self.gastos_por_periodo(inicio, fin)

    def total_gastos_mes_actual(self):

        gastos = self.gastos_mes_actual().aggregate(total=Sum('monto'))['total']

        if gastos is None:
            return Decimal()

        return gastos

    def porcentaje_ejecutado_mes_actual(self):

        return self.total_gastos_mes_actual() / max(self.limite, 1) * 100


@python_2_unicode_compatible
class Gasto(TimeStampedModel):
    """Representa las transacciones monetarias realizadas por el personal de la
    :class:`Ciudad` y que son restadas del :class:`Presupuesto` vigente"""
    cuenta = models.ForeignKey(Cuenta)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    cheque = models.CharField(max_length=255, blank=True, null=True)
    comprobante = models.FileField(upload_to='budget/gasto/%Y/%m/%d',
                                   blank=True, null=True)

    def __str__(self):
        return self.descripcion

    def get_absolute_url(self):
        return self.cuenta.get_absolute_url()
