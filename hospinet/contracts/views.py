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
from datetime import datetime, time

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, ListView, DetailView, DeleteView,
                                  TemplateView, UpdateView, FormView)
from guardian.decorators import permission_required

from contracts.forms import (PlanForm, ContratoForm, PagoForm, EventoForm,
                             VendedorForm, VendedorChoiceForm,
                             ContratoSearchForm)
from contracts.models import Contrato, Plan, Pago, Evento, Vendedor
from invoice.forms import PeriodoForm
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'contracts/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class PlanCreateView(CreateView, LoginRequiredMixin):
    model = Plan
    form_class = PlanForm


class PlanUpdateView(UpdateView, LoginRequiredMixin):
    model = Plan
    form_class = PlanForm


class PlanDetailView(DetailView, LoginRequiredMixin):
    model = Plan
    context_object_name = 'plan'


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


class ContratoCreateView(CreateView, PersonaFormMixin, LoginRequiredMixin):
    model = Contrato
    form_class = ContratoForm


class ContratoDetailView(DetailView, LoginRequiredMixin):
    model = Contrato
    context_object_name = 'contrato'


class ContratoUpdateView(UpdateView, LoginRequiredMixin):
    model = Contrato
    form_class = ContratoForm
    context_object_name = 'contrato'


class ContratoPeriodoView(TemplateView, LoginRequiredMixin):
    """Muestra los contratos de un periodo"""
    template_name = 'contracts/periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm()

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.contratos = Contrato.objects.filter(
                inicio__gte=self.inicio,
                inicio__lte=self.fin,
            )
        return super(ContratoPeriodoView, self).dispatch(request, *args,
                                                         **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContratoPeriodoView, self).get_context_data(**kwargs)

        context['contratos'] = self.contratos

        return context


class ContratoSearchView(FormView, LoginRequiredMixin):
    """Obtiene el primer :class:`Contrato` con el número especificado en el
    formulario"""
    form_class = ContratoSearchForm

    def form_valid(self, form):
        self.contrato = Contrato.objects.filter(
            numero=form.cleaned_data['numero']).first()
        return super(ContratoSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.contrato.get_absolute_url()


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


class VendedorCreateView(CreateView, LoginRequiredMixin):
    model = Vendedor
    form_class = VendedorForm


class VendedorDetailView(DetailView, LoginRequiredMixin):
    model = Vendedor
    context_object_name = 'vendedor'


class VendedorUpdateView(UpdateView, LoginRequiredMixin):
    model = Vendedor


class VendedorSearchView(FormView, LoginRequiredMixin):
    form_class = VendedorChoiceForm

    def form_valid(self, form):
        self.vendedor = Vendedor.objects.get(pk=form.cleaned_data['vendedor'])
        return super(VendedorSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.vendedor.get_absolute_url()
