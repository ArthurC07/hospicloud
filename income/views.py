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
from django.views.generic import CreateView, ListView, DetailView

from income.forms import ChequeCobroForm, DetallePagoForm
from income.models import Cheque, DetallePago
from invoice.models import CuentaPorCobrar
from users.mixins import LoginRequiredMixin


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
            form = ChequeCobroForm(
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


class ChequeCobroCreateView(CreateView, LoginRequiredMixin):
    """
    Creates a :class:`Cheque` based on the data obtained from the form, adds
    payment detail if the indicated amount matches the total amount from due
    payments
    """
    model = Cheque
    form_class = ChequeCobroForm

    def form_valid(self, form):

        self.object = form.save()
        if self.object.monto_total() == self.object.cuenta_por_cobrar.monto():
            for pago in self.object.cuenta_por_cobrar.payments().all():
                detalle = DetallePago()
                detalle.deposito = self.object
                detalle.monto = pago.monto
                detalle.pago = pago
                detalle.save()

        return self.get_success_url()


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
        for pago in self.object.cuenta_por_cobrar.payments().filter(
                completado=False):
            form = DetallePagoForm(initial={
                'pago': pago,
                'deposito': self.object,
                'monto': pago.monto
            })
            form.helper.form_action = 'detallepago-create'
            context['pagos'].append({
                'form': form,
                'pago': pago
            })

        return context


class DetallePagoCreateView(CreateView, LoginRequiredMixin):
    """
    Creates the :class:`DetallePago` based in the information handled by a
    :class:`DetallePagoForm`
    """
    model = DetallePago
    form_class = DetallePagoForm
