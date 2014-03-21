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

from crispy_forms.layout import Fieldset
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, ListView, DetailView, DeleteView,
                                  TemplateView, UpdateView, FormView)
from guardian.decorators import permission_required

from contracts.forms import (PlanForm, ContratoForm, PagoForm, EventoForm,
                             VendedorForm, VendedorChoiceForm,
                             ContratoSearchForm, PersonaForm, TipoEventoForm,
                             BeneficiarioForm, BeneficiarioPersonaForm)
from contracts.models import (Contrato, Plan, Pago, Evento, Vendedor,
                              TipoEvento, Beneficiario)
from invoice.forms import PeriodoForm
from persona.forms import PersonaSearchForm
from persona.models import Persona
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin


class ContratoPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('contracts.contrato'))
    def dispatch(self, *args, **kwargs):
        return super(ContratoPermissionMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView, ContratoPermissionMixin):
    template_name = 'contracts/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['vendedor-search'] = VendedorChoiceForm(
            prefix='vendedor-search')
        context['vendedor-search'].helper.form_action = 'vendedor-search'
        context['contrato-periodo'] = PeriodoForm(prefix='contrato-periodo')
        context['contrato-periodo'].helper.layout = Fieldset(
            "Contratos de un Periodo",
            *context['contrato-periodo'].field_names)
        context['contrato-periodo'].helper.form_action = 'contrato-periodo'
        context['contrato-search'] = ContratoSearchForm(
            prefix='contrato-search')
        context['contrato-search'].helper.form_action = 'contrato-search'
        context['contrato-persona-search'] = PersonaSearchForm(
            prefix='contrato-persona-search')
        context[
            'contrato-persona-search'].helper.form_action = 'contrato-persona-search'

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


class ContratoPersonaCreateView(CreateView, LoginRequiredMixin):
    model = Contrato
    template_name = 'contracts/contrato_create.html'

    def dispatch(self, request, *args, **kwargs):

        self.persona = Persona()

        self.ContratoFormset = inlineformset_factory(Persona, Contrato,
                                                     form=ContratoForm,
                                                     fk_name='persona', extra=1)
        return super(ContratoPersonaCreateView, self).dispatch(request, *args,
                                                               **kwargs)

    def get_form(self, form_class):
        formset = self.ContratoFormset(instance=self.persona, prefix='contrato')
        return formset

    def get_context_data(self, **kwargs):

        self.persona_form = PersonaForm(instance=self.persona, prefix='persona')
        self.persona_form.helper.form_tag = False

        context = super(ContratoPersonaCreateView, self).get_context_data(
            **kwargs)
        context['persona_form'] = self.persona_form
        return context

    def post(self, request, *args, **kwargs):
        self.persona_form = PersonaForm(request.POST, request.FILES,
                                        instance=self.persona,
                                        prefix='persona')
        self.formset = self.ContratoFormset(request.POST, request.FILES,
                                            instance=self.persona,
                                            prefix='contrato')

        if self.persona_form.is_valid() and self.formset.is_valid():
            self.persona_form.save()
            instances = self.formset.save()
            for instance in instances:
                self.contrato = instance
                self.contrato.save()

            return self.form_valid(self.formset)
        else:
            self.object = None
            return self.form_invalid(self.formset)

    def get_success_url(self):

        return reverse('contrato', args=[self.contrato.id])


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
        self.form = PeriodoForm(request.GET, prefix='contrato-periodo')

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
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context


class ContratoSearchView(FormView, LoginRequiredMixin):
    """Obtiene el primer :class:`Contrato` con el número especificado en el
    formulario"""
    form_class = ContratoSearchForm
    prefix = 'contrato-search'

    def form_valid(self, form):
        self.contrato = get_object_or_404(Contrato,
                                          numero=form.cleaned_data['numero'])
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
    prefix = 'vendedor-search'

    def form_valid(self, form):
        self.vendedor = form.cleaned_data['vendedor']
        return super(VendedorSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.vendedor.get_absolute_url()


class TipoEventoCreateView(CreateView, LoginRequiredMixin):
    model = TipoEvento
    form_class = TipoEventoForm


class BeneficiarioCreateView(CreateView, PersonaFormMixin, LoginRequiredMixin):
    model = Beneficiario
    form_class = BeneficiarioPersonaForm


class BeneficiarioPersonaCreateView(ContratoFormMixin):
    model = Beneficiario
    template_name = 'contracts/beneficiario_create.html'

    def dispatch(self, request, *args, **kwargs):

        self.persona = Persona()

        self.BeneficiarioFormset = inlineformset_factory(Persona, Beneficiario,
                                                         form=BeneficiarioForm,
                                                         fk_name='persona',
                                                         extra=1)
        return super(BeneficiarioPersonaCreateView, self).dispatch(request,
                                                                   *args,
                                                                   **kwargs)

    def get_form(self, form_class):
        formset = self.BeneficiarioFormset(instance=self.persona,
                                           prefix='beneficiario')

        for form in formset:
            form.initial['contrato'] = self.contrato
        return formset

    def get_context_data(self, **kwargs):

        self.persona_form = PersonaForm(instance=self.persona, prefix='persona')
        self.persona_form.helper.form_tag = False

        context = super(BeneficiarioPersonaCreateView, self).get_context_data(
            **kwargs)
        context['persona_form'] = self.persona_form
        return context

    def post(self, request, *args, **kwargs):
        self.persona_form = PersonaForm(request.POST, request.FILES,
                                        instance=self.persona,
                                        prefix='persona')
        self.formset = self.BeneficiarioFormset(request.POST, request.FILES,
                                                instance=self.persona,
                                                prefix='beneficiario')

        if self.persona_form.is_valid() and self.formset.is_valid():
            self.persona_form.save()
            self.formset.save()

            return self.form_valid(self.formset)
        else:
            self.object = None
            return self.form_invalid(self.formset)

    def get_success_url(self):

        return reverse('contrato', args=[self.contrato.id])


class BeneficiarioDeleteView(DeleteView, LoginRequiredMixin):
    model = Beneficiario

    def get_object(self, queryset=None):
        obj = super(BeneficiarioDeleteView, self).get_object(queryset)
        self.contrato = obj.contrato
        return obj

    def get_success_url(self):
        return self.contrato.get_absolute_url()


class ContratoPersonaSearchView(FormView, LoginRequiredMixin):
    """Obtiene el primer :class:`Contrato` con el número especificado en el
    formulario"""
    form_class = PersonaSearchForm
    prefix = 'contrato-persona-search'

    def form_valid(self, form):
        query = form.cleaned_data['query']
        queryset = Persona.objects.filter(
            Q(persona__nombre__icontains=query) |
            Q(persona__apellido__icontains=query) |
            Q(persona__identificacion__icontains=query)
        )

        self.contrato = queryset.first()

        if self.contrato is None:
            raise Http404

        return super(ContratoPersonaSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.contrato.get_absolute_url()
