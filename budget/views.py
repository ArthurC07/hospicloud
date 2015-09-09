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
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, ListView, DeleteView, \
    UpdateView, FormView, RedirectView, View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import FormMixin

from budget.forms import CuentaForm, GastoForm, GastoPendienteForm, \
    GastoEjecutarFrom, MontoForm
from budget.models import Presupuesto, Cuenta, Gasto, Income
from invoice.models import Venta
from users.mixins import LoginRequiredMixin
from hospinet.utils import get_current_month_range, get_previous_month_range


class PresupuestoDetailView(DetailView, LoginRequiredMixin):
    model = Presupuesto
    context_object_name = 'presupuesto'


class PresupuestoListView(ListView, LoginRequiredMixin):
    model = Presupuesto
    context_object_name = 'presupuestos'

    def get_queryset(self):
        return Presupuesto.objects.filter(inversion=False).all()

    def get_context_data(self, **kwargs):
        context = super(PresupuestoListView, self).get_context_data(**kwargs)

        fin, inicio = get_current_month_range()
        fin_prev, inicio_prev = get_previous_month_range()

        inversiones = Presupuesto.objects.filter(inversion=True)

        gastos = Gasto.objects.filter(
            fecha_de_pago__range=(inicio, fin),
            ejecutado=True,
            cuenta__presupuesto__inversion=False
        ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']

        presupuesto = Cuenta.objects.filter(
            presupuesto__activo=True,
            presupuesto__inversion=False
        ).aggregate(total=Coalesce(Sum('limite'), Decimal()))['total']

        context['presupuesto'] = presupuesto
        context['gastos'] = gastos

        context['porcentaje'] = gastos / max(presupuesto, 1) * 100
        ventas = Venta.objects.select_related('recibo').filter(
            recibo__created__range=(inicio, fin),
            recibo__nulo=False
        )

        credito = ventas.filter(recibo__credito=True).aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        ventas_anteriores = Venta.objects.select_related('recibo').filter(
            recibo__created__range=(inicio_prev, fin_prev),
            nulo=False
        )

        ingresos = ventas.values('recibo__ciudad__nombre').annotate(
            total=Coalesce(Sum('monto'), Decimal())
        ).order_by()

        disponible = ventas_anteriores.aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        total_ingresos = ventas.aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        context['total_ingresos'] = total_ingresos

        context['ingresos'] = ingresos
        context['inversiones'] = inversiones
        context['credito'] = credito

        context['equilibrio'] = gastos / max(context['total_ingresos'], 1)
        context['balance'] = total_ingresos - gastos
        context['disponible'] = disponible

        context['incomes'] = Income.objects.all()

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ejectuado = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class GastoPendienteCreateView(CuentaFormMixin, CreateView, LoginRequiredMixin):
    model = Gasto
    form_class = GastoPendienteForm


class GastoDeleteView(DeleteView, LoginRequiredMixin):
    """Permite eliminar un :class:`Gasto`"""
    model = Gasto

    def get_object(self, queryset=None):
        obj = super(GastoDeleteView, self).get_object(queryset)
        self.cuenta = obj.cuenta
        return obj

    def get_success_url(self):
        return self.cuenta.get_absolute_url()


class GastoEjecutarView(UpdateView, LoginRequiredMixin):
    model = Gasto
    form_class = GastoEjecutarFrom

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ejecutado = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class GastoScheduleView(RedirectView, LoginRequiredMixin):
    permanent = False

    def get_redirect_url(self, **kwargs):
        gasto = get_object_or_404(Gasto, pk=kwargs['pk'])
        gasto.schedule()

        return gasto.get_absolute_url()


class GastoMixin(ContextMixin, View):
    """
    Permite obtener un :class:`Gasto` desde los argumentos en una url
    """

    def dispatch(self, *args, **kwargs):
        self.gasto = get_object_or_404(Gasto, pk=kwargs['gasto'])
        return super(GastoMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GastoMixin, self).get_context_data(**kwargs)

        context['gasto'] = self.gasto

        return context


class GastoParcialFormView(GastoMixin, FormView, LoginRequiredMixin):
    """Permite efectuar un pago parcial a un :class:`Gasto`
    """
    form_class = MontoForm
    template_name = 'budget/gasto_form.html'

    def form_valid(self, form):

        self.gasto.pago_parcial(form.cleaned_data['monto'])

        return HttpResponseRedirect(self.gasto.get_absolute_url())
