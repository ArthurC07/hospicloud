#!/usr/bin/env python
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
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, DeleteView, \
    TemplateView, UpdateView
from contracts.forms import PlanForm, ContratoForm, PagoForm, EventoForm
from contracts.models import Contrato, Plan, Pago, Evento
from users.mixins import LoginRequiredMixin
from guardian.decorators import permission_required


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'contracts/index.html'


class PlanCreateView(CreateView, LoginRequiredMixin):
    model = Plan
    form_class = PlanForm


class PlanListView(ListView, LoginRequiredMixin):
    model = Plan
    context_object_name = 'planes'


class ContratoFormMixin(CreateView, LoginRequiredMixin):
    """Permite llenar el formulario de una clase que requiera
    :class:`Contrato`s de manera previa - DRY"""

    def get_context_data(self, **kwargs):
        context = super(ContratoFormMixin, self).get_context_data(**kwargs)
        context['contrato'] = self.contrato
        return context

    def get_initial(self):
        """Agrega el :class:`Contrato` obtenido como el valor a utilizar en el
        formulario que será llenado posteriormente"""
        initial = super(ContratoFormMixin, self).get_initial()
        initial = initial.copy()
        initial['contrato'] = self.contrato.id
        return initial

    @method_decorator(permission_required('contracts.contrato'))
    def dispatch(self, *args, **kwargs):
        """Obtiene el :class:`Contrato` que se entrego en la url"""

        self.contrato = get_object_or_404(Contrato, pk=kwargs['contrato'])
        return super(ContratoFormMixin, self).dispatch(*args, **kwargs)


class ContratoCreateView(CreateView, LoginRequiredMixin):
    model = Contrato
    form_class = ContratoForm


class ContratoDetailView(DetailView, LoginRequiredMixin):
    model = Contrato
    context_object_name = 'contrato'


class ContratoUpdateView(UpdateView, LoginRequiredMixin):
    model = Contrato
    form_class = ContratoForm
    context_object_name = 'contrato'


class PagoCreateView(ContratoFormMixin):
    model = Pago
    form_class = PagoForm


class PagoDeleteView(DeleteView, LoginRequiredMixin):
    model = Pago

    def get_object(self, queryset=None):
        obj = super(PagoDeleteView, self).get_object(queryset)
        self.contrato = obj.contrato
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        self.contrato.ultimo_pago = self.contrato.pagos[:-1].fecha

        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.contrato.get_absolute_url()


class EventoCreateView(ContratoFormMixin):
    model = Evento
    form_class = EventoForm


class EventoDeleteView(DeleteView, LoginRequiredMixin):
    model = Evento

    def get_object(self, queryset=None):
        obj = super(EventoDeleteView, self).get_object(queryset)
        self.contrato = obj.contrato
        return obj

    def get_success_url(self):
        return self.contrato.get_absolute_url()
