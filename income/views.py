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
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from hospinet.utils.forms import NumeroForm
from income.forms import ChequeForm, DetallePagoForm, DepositoForm, \
    CierrePOSForm
from income.models import Cheque, DetallePago, Deposito, CierrePOS
from invoice.models import CuentaPorCobrar, Pago
from users.mixins import LoginRequiredMixin


class IncomeIndexView(TemplateView, LoginRequiredMixin):
    """
    Shows the forms associated with income related querys
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
                initial={'usuario': self.request.user}
        )
        context['cierre_form'].helper.form_action = 'cierre-create'

        return context


class CobrosListView(ListView, LoginRequiredMixin):
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


class DepositoDetailView(DetailView, LoginRequiredMixin):
    """
    Creates the UI to visualize the data gathered by a :class:`Deposito`
    """
    model = Deposito


class DepositoCreateView(CreateView, LoginRequiredMixin):
    """
    Allows the user to create a :class:`Deposito`
    """
    model = Deposito
    form_class = DepositoForm


class ChequeCreateView(CreateView, LoginRequiredMixin):
    """
    Creates a :class:`Cheque` based on the data obtained from the form, adds
    payment detail if the indicated amount matches the total amount from due
    payments
    """
    model = Cheque
    form_class = ChequeForm


class ChequeCobroDetailView(DetailView, LoginRequiredMixin):
    """
    Shows the GUI with the data from the payments that require consolidation,
    adding the forms that collect the information related to each :class:`Pago`
    """
    model = Cheque

    def get_context_data(self, **kwargs):
        """
        Builds the data that will be shown in the GUI
        :param kwargs: dictionary with data arguments
        :return: The dictionary with the built data
        """
        context = super(ChequeCobroDetailView, self).get_context_data(**kwargs)

        context['pagos'] = []
        for pago in Pago.objects.filter(status__pending=True, completado=False,
                                        tipo__reembolso=True):
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

        return context


class CierrePOSCreateView(CreateView, LoginRequiredMixin):
    """
    Enables creation of :class:`CierrePOS` from the user interface.
    """
    model = CierrePOS
    form_class = CierrePOSForm


class ChequeNumeroListView(ListView, LoginRequiredMixin):
    """
    Enables searching :class:`Cheque` by using their number field
    """
    context_object_name = 'cheques'

    def get_queryset(self):
        form = NumeroForm(self.request.GET)
        if form.is_valid():
            return Cheque.objects.filter(
                    numero_de_cheque__contains=form.cleaned_data['numero']
            )
        return Cheque.objects.all()


class DetallePagoCreateView(CreateView, LoginRequiredMixin):
    """
    Creates the :class:`DetallePago` based in the information handled by a
    :class:`DetallePagoForm`
    """
    model = DetallePago
    form_class = DetallePagoForm
