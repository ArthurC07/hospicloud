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
from __future__ import unicode_literals

from datetime import date, datetime
from decimal import Decimal

from crispy_forms.layout import Submit
from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Sum, Max
from django.db.models.functions import Coalesce
from django.forms.widgets import HiddenInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, CreateView, ListView, DeleteView, \
    UpdateView, FormView, RedirectView, View, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from budget.forms import CuentaForm, GastoForm, GastoPendienteForm, \
    GastoEjecutarFrom, MontoForm, GastoPeriodoCuentaForm, \
    GastoPresupuestoPeriodoCuentaForm, PresupuestoMesForm
from budget.models import Presupuesto, Cuenta, Gasto, Income, PresupuestoMes, \
    Fuente
from hospinet.utils import get_current_month_range, get_previous_month_range
from hospinet.utils.date import get_month_end, make_end_day
from hospinet.utils.forms import YearForm, MonthYearForm, PeriodoForm
from income.models import Deposito, Cheque
from invoice.models import Venta, Pago
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class PresupuestoDetailView(LoginRequiredMixin, DetailView):
    """
    Shows a :class:`Presupuesto` detailed data view, describing the accounting
    break up from every expense category.
    """
    model = Presupuesto
    context_object_name = 'presupuesto'
    queryset = Presupuesto.objects.select_related(
            'ciudad'
    ).prefetch_related(
            'cuenta_set',
    )


class PresupuestoListView(LoginRequiredMixin, ListView):
    """
    Allows viewing data related to all :class:`Presupuesto`s in the
    :class:`Company`.
    """
    model = Presupuesto
    context_object_name = 'presupuestos'
    queryset = Presupuesto.objects.prefetch_related(
            'cuenta_set',
    ).select_related(
            'ciudad'
    ).filter(inversion=False)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoListView, self).get_context_data(**kwargs)

        fin, inicio = get_current_month_range()
        fin_prev, inicio_prev = get_previous_month_range()

        inversiones = Presupuesto.objects.select_related(
                'ciudad'
        ).filter(inversion=True)

        gastos = Gasto.objects.select_related(
                'cuenta',
                'cuenta__presupuesto',
                'cuenta__presupuesto__ciudad',
        ).filter(
                fecha_de_pago__range=(inicio, fin),
                ejecutado=True,
                cuenta__presupuesto__inversion=False
        ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']

        presupuesto = Cuenta.objects.select_related('presupuesto').filter(
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
                recibo__nulo=False
        )

        context['credito_anterior'] = ventas_anteriores.filter(
                recibo__credito=True
        ).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        context['contado_anterior'] = ventas_anteriores.filter(
                recibo__credito=False
        ).aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        ingresos = ventas.select_related(
                'recibo__ciudad'
        ).values(
                'recibo__ciudad__nombre'
        ).annotate(
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

        context['gasto-periodo'] = GastoPeriodoCuentaForm(
                prefix='gasto-cuenta-periodo')
        context['gasto-periodo'].set_action('gasto-periodo')

        context[
            'gasto-presupuesto-periodo'] = GastoPresupuestoPeriodoCuentaForm(
                prefix='gasto-presupuesto-periodo'
        )
        context['gasto-presupuesto-periodo'].set_action(
                'gasto-presupuesto-periodo'
        )

        context['budget-month'] = PresupuestoMesForm()
        context['budget-month'].set_action('monthly-budget-add')

        context['budget-month-year'] = MonthYearForm()
        context['budget-month-year'].set_action('budget-list')
        context['budget-month-year'].set_legend(
                _('Revisar Presupuesto del Mes')
        )
        context['budget-month-year'].helper.form_method = 'get'
        context['budget-month-year'].helper.add_input(
                Submit('submit', _('Mostrar')))

        context['balance-month-year'] = MonthYearForm()
        context['balance-month-year'].set_action('budget-balance-monthly')
        context['balance-month-year'].set_legend(
                _('Mostrar Balance del Mes')
        )
        context['balance-month-year'].helper.form_method = 'get'
        context['balance-month-year'].helper.add_input(
                Submit('submit', _('Mostrar')))

        year = timezone.now().year

        context['budget_forms'] = []

        for n in range(1, 13):
            form = MonthYearForm(initial={
                'year': year,
                'mes': n,
            })
            form.helper.attrs = {'target': '_blank'}
            form.set_action('budget-balance-monthly')
            form.fields['year'].widget = HiddenInput()
            form.fields['mes'].widget = HiddenInput()
            form.helper.form_method = 'get'
            form.helper.add_input(Submit(
                    'submit',
                    _('{0} de {1}'.format(n, year))
            ))
            context['budget_forms'].append(form)

        return context


class PresupuestoMixin(ContextMixin, View):
    """
    Permite obtener un :class:`Cotizacion` desde los argumentos en una url
    """

    def dispatch(self, *args, **kwargs):
        self.presupuesto = get_object_or_404(Presupuesto,
                                             pk=kwargs['presupuesto'])
        return super(PresupuestoMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoMixin, self).get_context_data(**kwargs)

        context['presupuesto'] = self.presupuesto

        return context


class PresupuestoFormMixin(PresupuestoMixin, FormMixin):
    """
    Permite inicializar el :class:`Presupuesto` que se utilizará en un
    formulario
    """

    def get_initial(self):
        initial = super(PresupuestoFormMixin, self).get_initial()
        initial = initial.copy()
        initial['presupuesto'] = self.presupuesto
        return initial


class CuentaDetailView(LoginRequiredMixin, DetailView):
    """
    Allows the user to review the data of a :class:`Cuenta`
    """
    model = Cuenta
    context_object_name = 'cuenta'


class CuentaCreateView(PresupuestoFormMixin, LoginRequiredMixin, CreateView):
    """
    Allows the user to create :class:`Cuenta` objects
    """
    model = Cuenta
    form_class = CuentaForm


class CuentaMixin(ContextMixin, View):
    """Permite obtener un :class:`Cotizacion` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.cuenta = get_object_or_404(Cuenta, pk=kwargs['cuenta'])
        return super(CuentaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CuentaMixin, self).get_context_data(**kwargs)
        context['cuenta'] = self.cuenta
        return context


class CuentaFormMixin(CuentaMixin, FormMixin):
    """
    Permite inicializar el :class:`Presupuesto` que se utilizará en un
    formulario
    """

    def get_initial(self):
        initial = super(CuentaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['cuenta'] = self.cuenta
        return initial


class GastoCreateView(CuentaFormMixin, CreateView, CurrentUserFormMixin,
                      LoginRequiredMixin):
    """
    Allows the user to create a :class:`Gasto`
    """
    model = Gasto
    form_class = GastoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ejecutar()

        return HttpResponseRedirect(self.get_success_url())


class GastoPendienteCreateView(CuentaFormMixin, CreateView,
                               CurrentUserFormMixin, LoginRequiredMixin):
    model = Gasto
    form_class = GastoPendienteForm


class GastoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Permite eliminar un :class:`Gasto`
    """
    model = Gasto

    def get_object(self, queryset=None):
        obj = super(GastoDeleteView, self).get_object(queryset)
        self.cuenta = obj.cuenta
        return obj

    def get_success_url(self):
        return self.cuenta.get_absolute_url()


class GastoEjecutarView(LoginRequiredMixin, UpdateView):
    """
    Allows a :class:`Gasto` to be marked as completed
    """
    model = Gasto
    form_class = GastoEjecutarFrom

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ejecutar()

        return HttpResponseRedirect(self.get_success_url())


class GastoScheduleView(LoginRequiredMixin, RedirectView):
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


class GastoParcialFormView(GastoMixin, LoginRequiredMixin, FormView):
    """Permite efectuar un pago parcial a un :class:`Gasto`
    """
    form_class = MontoForm
    template_name = 'budget/gasto_form.html'

    def form_valid(self, form):
        self.gasto.pago_parcial(form.cleaned_data['monto'])

        return HttpResponseRedirect(self.gasto.get_absolute_url())


class GastoCuentaPeriodoView(FormMixin, LoginRequiredMixin, TemplateView):
    """
    Obtiene los :class:`Gastos` de un periodo y cuenta determinados
    """
    form_class = GastoPeriodoCuentaForm
    prefix = 'gasto-cuenta-periodo'
    template_name = 'budget/gasto_list.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Efectua la consulta de los :class:`Gastos` de acuerdo a los
        datos ingresados en el formulario
        """

        self.form = self.get_form_class()(request.GET, prefix=self.prefix)

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.cuenta = self.form.cleaned_data['cuenta']
            self.gastos = Gasto.objects.filter(
                    cuenta=self.cuenta,
                    fecha_de_pago__range=(self.inicio, self.fin),
                    ejecutado=True
            ).select_related('proveedor', 'usuario').all()
        else:
            messages.info(
                    self.request,
                    _('Los Datos Ingresados en el formulario no son validos')
            )
            return HttpResponseRedirect(reverse('invoice-index'))

        return super(GastoCuentaPeriodoView, self).dispatch(request, *args,
                                                            **kwargs)

    def get_context_data(self, **kwargs):

        context = super(GastoCuentaPeriodoView, self).get_context_data(**kwargs)

        context['gastos'] = self.gastos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = self.gastos.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']
        context['motivo'] = self.cuenta

        return context


class GastoPeriodoListView(LoginRequiredMixin, ListView):
    """
    Builds a list of :class:`Gasto`s that have been registered during
    """
    model = Gasto
    context_object_name = 'gastos'

    def get_queryset(self):
        """
        Filters the :class:`Gasto` objects
        :return: a filtered :class:`QuerySet`
        """
        form = PeriodoForm(self.request.GET)
        if form.is_valid():
            return Gasto.objects.filter(
                    fecha_de_pago__range=(
                        form.cleaned_data['inicio'],
                        form.cleaned_data['fin']
                    ),
                    ejecutado=True
            ).select_related('proveedor', 'usuario')
        return Gasto.objects.select_related('proveedor', 'usuario').all()

    def get_context_data(self, **kwargs):
        context = super(GastoPeriodoListView, self).get_context_data(**kwargs)
        context['total'] = self.get_queryset().aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return context


class GastoPresupuestoPeriodoView(FormMixin, LoginRequiredMixin, TemplateView):
    """
    Obtiene los :class:`Gastos` de un periodo y cuenta determinados
    """
    form_class = GastoPresupuestoPeriodoCuentaForm
    prefix = 'gasto-presupuesto-periodo'
    template_name = 'budget/gasto_list.html'

    def dispatch(self, request, *args, **kwargs):
        """Efectua la consulta de los :class:`Gastos` de acuerdo a los
        datos ingresados en el formulario"""

        self.form = self.get_form_class()(request.GET, prefix=self.prefix)

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.presupuesto = self.form.cleaned_data['presupuesto']
            self.gastos = Gasto.objects.filter(
                    cuenta__presupuesto=self.presupuesto,
                    fecha_de_pago__range=(self.inicio, self.fin),
                    ejecutado=True
            ).all()
        else:
            messages.info(
                    self.request,
                    _('Los Datos Ingresados en el formulario no son validos')
            )
            return HttpResponseRedirect(reverse('invoice-index'))

        return super(GastoPresupuestoPeriodoView, self).dispatch(request, *args,
                                                                 **kwargs)

    def get_context_data(self, **kwargs):
        """
        Allows adding the calculated data into the template
        :param kwargs: 
        :return: The context that will be rendered in the template
        """
        context = super(GastoPresupuestoPeriodoView, self).get_context_data(
                **kwargs)

        context['gastos'] = self.gastos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = self.gastos.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']
        context['motivo'] = self.presupuesto

        return context


class PresupuestoAnualView(TemplateView, LoginRequiredMixin):
    """
    Shows the data related to the :class:`PresupuestoMes`
    """
    template_name = 'budget/anual.html'

    def get_context_data(self, **kwargs):
        context = super(PresupuestoAnualView, self).get_context_data(**kwargs)
        form = YearForm(self.request.GET)

        if form.is_valid():
            year = form.cleaned_data['year']
            context['year'] = year
            context['presupuesto'] = PresupuestoMes.objects.filter(
                    anio=year
            ).values(
                    'mes', 'anio',
            ).annotate(
                    total=Coalesce(Sum('monto'), Decimal())
            ).order_by()
            context['total'] = PresupuestoMes.objects.filter(
                    anio=year
            ).aggregate(total=Coalesce(Sum('monto'), Decimal()))['total']
            context['mayor'] = PresupuestoMes.objects.filter(
                    anio=year
            ).aggregate(Max('monto'))

        return context


class PresupuestoMesListView(LoginRequiredMixin, ListView):
    """
    Shows a list of :class:`PresupuestoMes`
    """
    model = PresupuestoMes

    def get_queryset(self):
        """
        Filters the :class:`PresupuestoMes` according to the
        :class:`MonthYearForm`
        :return: the filtered :class:`QuerySet`
        """
        form = MonthYearForm(self.request.GET)
        if form.is_valid():
            self.year = form.cleaned_data['year']
            self.mes = form.cleaned_data['mes']
            return PresupuestoMes.objects.filter(
                    anio=self.year,
                    mes=self.mes,
            )
        return PresupuestoMes.objects.all()

    def get_context_data(self, **kwargs):
        """
        Builds the forms that will correct the :class:`PresupuestoMes` data
        :param kwargs:
        :return:
        """
        context = super(PresupuestoMesListView, self).get_context_data(**kwargs)

        context['forms'] = []
        context['fecha'] = date(self.year, self.mes, 1)
        for presupuesto in self.object_list.all():
            form = PresupuestoMesForm(instance=presupuesto)
            form.fields['completar_anio'].widget = forms.HiddenInput()
            form.fields['anio'].widget = forms.HiddenInput()
            form.fields['mes'].widget = forms.HiddenInput()
            context['forms'].append(form)

        return context


class PresupuestoMesDetailView(LoginRequiredMixin, DetailView):
    """
    Allows displaying the data for :class:`PresupuestoMes` instances
    """
    model = PresupuestoMes


class PresupuestoMesCreateView(LoginRequiredMixin, CreateView):
    """
    Creates :class:`PresupuestoMes` instances based on data entered into a
    :class:`PresupuestoMesForm`
    """
    model = PresupuestoMes
    form_class = PresupuestoMesForm

    def get_success_url(self):
        """
        :return: URL to create new :class:`PresupuestoMes`
        """
        return reverse('monthly-budget-add')


class PresupuestoMesUpdateView(LoginRequiredMixin, UpdateView):
    """
    Updates the :class:`PresupuestoMes` instances
    """
    model = PresupuestoMes
    form_class = PresupuestoMesForm


class BalanceView(TemplateView, LoginRequiredMixin):
    """
    Builds a view that resumes income and expenses for a given month
    """
    template_name = 'budget/balance_month.html'

    def dispatch(self, request, *args, **kwargs):

        form = MonthYearForm(request.GET)

        if form.is_valid():
            self.year = form.cleaned_data['year']
            self.mes = form.cleaned_data['mes']
        else:
            messages.info(
                    self.request,
                    _('Los Datos Ingresados en el formulario no son válidos')
            )
            return HttpResponseRedirect(reverse('budget-index'))

        return super(BalanceView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Builds the forms that will correct the :class:`PresupuestoMes` data
        :param kwargs: The original dictionary with data
        :return: the final dict that will be used in the view
        """
        context = super(BalanceView, self).get_context_data(**kwargs)

        context['forms'] = []
        inicio = timezone.make_aware(datetime(self.year, self.mes, 1))
        fin = make_end_day(get_month_end(inicio))

        context['fecha'] = inicio

        cuentas = Fuente.objects.filter(caja=False)

        context['cuentas'] = cuentas
        context['saldo_cuentas'] = cuentas.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        depositos = Deposito.objects.filter(
                fecha_de_deposito__range=(inicio, fin)
        )

        total_depositado = depositos.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        context['total_depositado'] = total_depositado

        context['descripcion_depositos'] = depositos.values(
                'tipo__nombre'
        ).annotate(total=Coalesce(Sum('monto'), Decimal())).order_by()

        gastos = Gasto.objects.filter(
                fecha_de_pago__range=(inicio, fin),
                ejecutado=True
        )

        total_gastos = gastos.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        context['gastos'] = gastos.order_by('-monto')

        context['total_gastos'] = total_gastos

        context['balance'] = total_depositado - total_gastos

        cheques = Cheque.objects.filter(
                fecha_de_entrega__range=(inicio, fin)
        )

        context['descripcion_cheques'] = cheques.values(
                'tipo__nombre'
        ).annotate(total=Coalesce(Sum('monto'), Decimal())).order_by()

        context['total_cheques'] = cheques.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        presupuesto = PresupuestoMes.objects.filter(
                anio=self.year,
                mes=self.mes,
        )

        context['presupuestos'] = presupuesto

        context['presupuestado'] = presupuesto.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        context['presupuestado_ciudad'] = presupuesto.values(
                'cuenta__presupuesto__ciudad__nombre'
        ).annotate(
                total=Coalesce(Sum('monto'), Decimal())
        ).order_by()

        context['periodo_string'] = urlencode(
                {
                    'inicio': inicio.strftime('%d/%m/%Y %H:%M'),
                    'fin': fin.strftime('%d/%m/%Y %H:%M'),
                    'submit': 'Mostrar'
                }
        )

        ventas = Venta.objects.select_related(
                'recibo',
                'item'
        ).filter(
                recibo__created__range=(inicio, fin)
        )

        context['total_ventas'] = ventas.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total']

        pagos = Pago.objects.select_related(
                'tipo',
        ).filter(
                recibo__created__range=(inicio, fin)
        )

        context['pagos'] = pagos.values(
                'tipo__nombre'
        ).annotate(
                total=Coalesce(Sum('monto'), Decimal())
        ).order_by()

        return context
