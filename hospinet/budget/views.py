# -*- coding: utf-8 -*-
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, ListView
from django.views.generic.base import TemplateResponseMixin

from django.views.generic.edit import FormMixin

from budget.forms import CuentaForm, GastoForm
from budget.models import Presupuesto, Cuenta, Gasto
from invoice.models import Venta
from users.mixins import LoginRequiredMixin
from users.models import get_current_month_range


class PresupuestoDetailView(DetailView, LoginRequiredMixin):
    model = Presupuesto
    context_object_name = 'presupuesto'


class PresupuestoListView(ListView, LoginRequiredMixin):
    model = Presupuesto
    context_object_name = 'presupuestos'

    def get_queryset(self):

        return Presupuesto.objects.all()

    def get_context_data(self, **kwargs):

        context = super(PresupuestoListView, self).get_context_data(**kwargs)

        fin, inicio = get_current_month_range()

        gastos = Gasto.objects.filter(
            created__range=(inicio, fin)
        ).aggregate(total=Sum('monto'))['total']

        presupuesto = Cuenta.objects.filter(
            presupuesto__activo=True
        ).aggregate(total=Sum('limite'))['total']

        if presupuesto is None:
            presupuesto = Decimal()

        if gastos is None:
            gastos = Decimal()

        context['presupuesto'] = presupuesto
        context['gastos'] = gastos

        context['porcentaje'] = gastos / max(presupuesto, 1) * 100
        ventas = Venta.objects.select_related('recibo').filter(
            recibo__created__range=(inicio, fin)
        )

        ingresos = ventas.values('recibo__ciudad__nombre').annotate(
            total=Sum('monto')
        ).order_by()
        context['total_ingresos'] = ventas.aggregate(total=Sum('monto'))['total']

        context['ingresos'] = ingresos

        context['equilibrio'] = gastos / max(context['total_ingresos'], 1)
        context['balance'] = context['total_ingresos'] - gastos

        return context


class PresupuestoMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Cotizacion` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.presupuesto = get_object_or_404(Presupuesto,
                                             pk=kwargs['presupuesto'])
        return super(PresupuestoMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoMixin, self).get_context_data(**kwargs)

        context['presupuesto'] = self.presupuesto

        return context


class PresupuestoFormMixin(PresupuestoMixin, FormMixin):
    """Permite inicializar el :class:`Presupuesto` que se utilizará en un
    formulario"""

    def get_initial(self):
        initial = super(PresupuestoFormMixin, self).get_initial()
        initial = initial.copy()
        initial['presupuesto'] = self.presupuesto
        return initial


class CuentaDetailView(DetailView, LoginRequiredMixin):
    model = Cuenta
    context_object_name = 'cuenta'


class CuentaCreateView(PresupuestoFormMixin, CreateView, LoginRequiredMixin):
    model = Cuenta
    form_class = CuentaForm


class CuentaMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Cotizacion` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.cuenta = get_object_or_404(Cuenta, pk=kwargs['cuenta'])
        return super(CuentaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CuentaMixin, self).get_context_data(**kwargs)

        context['cuenta'] = self.cuenta

        return context


class CuentaFormMixin(CuentaMixin, FormMixin):
    """Permite inicializar el :class:`Presupuesto` que se utilizará en un
    formulario"""

    def get_initial(self):
        initial = super(CuentaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['cuenta'] = self.cuenta
        return initial


class GastoCreateView(CuentaFormMixin, CreateView, LoginRequiredMixin):
    model = Gasto
    form_class = GastoForm
