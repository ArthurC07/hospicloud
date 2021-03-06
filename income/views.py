# -*- coding: utf-8 -*-
#
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

from decimal import Decimal

from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from hospinet.utils.forms import NumeroForm, PeriodoForm
from income.forms import ChequeForm, DetallePagoForm, DepositoForm, \
    CierrePOSForm
from income.models import Cheque, DetallePago, Deposito, CierrePOS, TipoDeposito
from invoice.models import CuentaPorCobrar, Pago
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class IncomeIndexView(TemplateView, LoginRequiredMixin):
    """
    Shows the forms associated with income related queries
    """
    template_name = 'income/index.html'

    def get_context_data(self, **kwargs):
        context = super(IncomeIndexView, self).get_context_data(**kwargs)

        context['cheque_form'] = ChequeForm(
            initial={'usuario': self.request.user}
        )
        context['cheque_form'].helper.form_action = 'cheque-create'

        context['numero_form'] = NumeroForm()
        context['numero_form'].set_legend(_('Buscar Cheque por Número'))
        context['numero_form'].helper.form_method = 'get'
        context['numero_form'].set_action('cheque-numero')

        context['deposito_form'] = DepositoForm(
            initial={'usuario': self.request.user}
        )
        context['deposito_form'].helper.form_action = 'deposito-create'

        context['cierre_form'] = CierrePOSForm(
            initial={'usuario': self.request.user},
            prefix='cierrepos',
        )
        context['cierre_form'].helper.form_action = 'cierre-create'

        return context


class CobrosListView(LoginRequiredMixin, ListView):
    """
    Shows the list of :class:`CuentaPorCobrar` and builds the forms to pay them
    """
    model = CuentaPorCobrar
    template_name = 'income/cuentaporcobrarpagar_list.html'

    def get_queryset(self):
        return CuentaPorCobrar.objects.filter(status__pending=True)

    def get_context_data(self, **kwargs):
        """
        Builds the actual list of due payments and the forms to associate a
        :class:`Cheque` to them.
        :param kwargs:
        :return: Template context data containing the list.
        """
        context = super(CobrosListView, self).get_context_data(**kwargs)

        objects = []
        for cuenta in self.object_list.all():
            form = ChequeForm(
                initial={'cuenta_por_cobrar': cuenta,
                         'usuario': self.request.user}
            )
            form.helper.form_action = 'cheque-create'
            objects.append({
                'cuenta': cuenta,
                'form': form
            })

        context['cuentas'] = objects
        context['cheques'] = Cheque.objects.all()

        return context


class DepositoDetailView(LoginRequiredMixin, DetailView):
    """
    Creates the UI to visualize the data gathered by a :class:`Deposito`
    """
    model = Deposito


class DepositoCreateView(CurrentUserFormMixin, CreateView):
    """
    Allows the user to create a :class:`Deposito`
    """
    model = Deposito
    form_class = DepositoForm

    def get_success_url(self):
        """
        Tells the program that the user should be redirected to the income index
        page.
        :return: The :class:`IncomeIndexView` url
        """
        if self.request.META['HTTP_REFERER']:
            messages.info(
                self.request,
                "Deposito de {0} Agregado".format(self.object.monto)
            )
            return self.request.META['HTTP_REFERER']
        else:
            return 'income-index'


class DepositoPeriodoListView(LoginRequiredMixin, ListView):
    """
    Builds a list of :class:`Deposito`s that have been registered during
    """
    model = Deposito
    context_object_name = 'depositos'

    def get_queryset(self):
        """
        Filters the :class:`Deposito` objects
        :return: a filtered :class:`QuerySet`
        """
        form = PeriodoForm(self.request.GET)
        if form.is_valid():
            return Deposito.objects.filter(
                fecha_de_deposito__range=(
                    form.cleaned_data['inicio'],
                    form.cleaned_data['fin']
                )
            ).select_related(
                'cuenta',
                'usuario'
            ).order_by('fecha_de_deposito')
        return Deposito.objects.select_related(
            'cuenta',
            'usuario'
        ).all().order_by('fecha_de_deposito')

    def get_context_data(self, **kwargs):
        context = super(DepositoPeriodoListView, self).get_context_data(
            **kwargs)

        context['total'] = self.get_queryset().aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return context


class ChequeCreateView(LoginRequiredMixin, CreateView):
    """
    Creates a :class:`Cheque` based on the data obtained from the form, adds
    payment detail if the indicated amount matches the total amount from due
    payments
    """
    model = Cheque
    form_class = ChequeForm


class ChequeCobroDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the GUI with the data from the payments that require consolidation,
    adding the forms that collect the information related to each :class:`Pago`
    """
    model = Cheque
    queryset = Cheque.objects.prefetch_related(
        'detallepago_set',
        'detallepago_set__pago',
        'detallepago_set__pago__recibo',
        'detallepago_set__pago__recibo__ciudad',
        'detallepago_set__pago__aseguradora',
    )

    def get_context_data(self, **kwargs):
        """
        Builds the data that will be shown in the GUI
        :param kwargs: dictionary with data arguments
        :return: The dictionary with the built data
        """
        context = super(ChequeCobroDetailView, self).get_context_data(**kwargs)

        context['pagos'] = []
        pagos = Pago.objects.cuentas_por_cobrar().select_related(
            'recibo',
            'aseguradora',
            'recibo__cliente',
            'recibo__ciudad',
            'recibo__legal_data',
        )
        for pago in pagos:
            form = DetallePagoForm(initial={
                'pago': pago,
                'cheque': self.object,
                'monto': pago.monto
            })
            form.helper.form_action = 'detallepago-create'
            context['pagos'].append({
                'form': form,
                'pago': pago
            })

        context['cantidad'] = pagos.count()

        return context


class ChequePeriodoListView(LoginRequiredMixin, ListView):
    """
    Shows a GUI with a list of :class:`Cheque` that have been registered during
    the period of time indicated by a :class:`PeriodoForm`
    """
    model = Cheque
    context_object_name = 'cheques'

    def get_queryset(self):
        """
        Filters the :class:`Cheque` objects
        :return: a filtered :class:`QuerySet`
        """
        form = PeriodoForm(self.request.GET)
        if form.is_valid():
            return Cheque.objects.filter(
                fecha_de_entrega__range=(
                    form.cleaned_data['inicio'],
                    form.cleaned_data['fin']
                )
            ).select_related(
                'usuario',
                'banco_de_emision',
                'usuario'
            ).prefetch_related(
                'detallepago_set',
                'detallepago_set__pago',
                'detallepago_set__pago__aseguradora',
                'detallepago_set__pago__recibo',
                'detallepago_set__pago__recibo__ciudad',
            ).order_by('fecha_de_entrega')
        return Cheque.objects.select_related(
            'usuario',
            'banco_de_emision',
            'usuario'
        ).prefetch_related(
            'detallepago_set',
            'detallepago_set__pago',
            'detallepago_set__pago__aseguradora',
            'detallepago_set__pago__recibo',
            'detallepago_set__pago__recibo__ciudad',
        ).all().order_by('fecha_de_entrega')

    def get_context_data(self, **kwargs):
        context = super(ChequePeriodoListView, self).get_context_data(**kwargs)

        context['total'] = self.get_queryset().aggregate(
            total=Coalesce(Sum('monto'), Decimal())
        )['total']

        return context


class CierrePOSCreateView(LoginRequiredMixin, CreateView):
    """
    Enables creation of :class:`CierrePOS` from the user interface.
    """
    model = CierrePOS
    form_class = CierrePOSForm
    prefix = 'cierrepos'


class ChequeNumeroListView(LoginRequiredMixin, ListView):
    """
    Enables searching :class:`Cheque` by using their number field
    """
    context_object_name = 'cheques'

    def get_queryset(self):
        form = NumeroForm(self.request.GET)
        if form.is_valid():
            return Cheque.objects.select_related('banco_de_emision').filter(
                numero_de_cheque__contains=form.cleaned_data['numero']
            )
        return Cheque.objects.all()


class DetallePagoCreateView(LoginRequiredMixin, CreateView):
    """
    Creates the :class:`DetallePago` based in the information handled by a
    :class:`DetallePagoForm`
    """
    model = DetallePago
    form_class = DetallePagoForm


class TipoDepositoDetailView(LoginRequiredMixin, DetailView):
    """
    Shows a GUI with a list of :class:`Deposito` corresponding to a
    :class:`TipoDeposito` that have been registered during the period of time
    indicated by a :class:`PeriodoForm`
    """
    model = TipoDeposito
    queryset = TipoDeposito.objects.prefetch_related(
        'deposito_set',
    )

    def get_context_data(self, **kwargs):
        context = super(TipoDepositoDetailView, self).get_context_data(
            **kwargs)

        form = PeriodoForm(self.request.GET)
        if form.is_valid():
            depositos = self.object.deposito_set.filter(
                fecha_de_deposito__range=(
                    form.cleaned_data['inicio'],
                    form.cleaned_data['fin']
                )
            ).select_related(
                'usuario',
                'cuenta'
            )

            context['depositos'] = depositos

            context['total'] = depositos.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
            )['total']

        return context
