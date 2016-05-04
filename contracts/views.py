# !/usr/bin/env python
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
from __future__ import unicode_literals

import calendar
from datetime import datetime, time

from crispy_forms.layout import Submit, Layout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum, Avg, Count
from django.db.models.functions import Coalesce
from django.forms import HiddenInput
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, DetailView, DeleteView, \
    TemplateView, UpdateView, FormView, View
from django.views.generic.base import RedirectView, ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from extra_views import InlineFormSet, CreateWithInlinesView

from bsc.models import Queja, Voto
from clinique.models import Cita, Consulta, Seguimiento, Incapacidad
from contracts.forms import PlanForm, ContratoForm, PagoForm, EventoForm, \
    VendedorForm, VendedorChoiceForm, ContratoSearchForm, PersonaForm, \
    TipoEventoForm, BeneficiarioForm, BeneficiarioPersonaForm, \
    LimiteEventoForm, PlanChoiceForm, MetaForm, CancelacionForm, \
    ContratoEmpresarialForm, EmpleadorChoiceForm, VendedorPeriodoForm, \
    PrecontratoForm, PersonaPrecontratoForm, BeneficioForm, \
    MasterContractForm, ImportFileForm, ContratoMasterForm, PCDForm, \
    AseguradoraForm, AseguradoraPeriodoForm
from contracts.models import Contrato, Plan, Pago, Evento, Vendedor, \
    TipoEvento, Beneficiario, LimiteEvento, Meta, Cancelacion, Precontrato, \
    Prebeneficiario, Beneficio, MasterContract, ImportFile, PCD, Aseguradora
from hospinet.utils import get_current_month_range
from hospinet.utils.date import make_month_range
from invoice.forms import PeriodoForm
from invoice.models import Venta
from persona.forms import PersonaForm as ButtonPersonaForm
from persona.forms import PersonaSearchForm
from persona.models import Persona, Empleador
from persona.views import PersonaFormMixin
from spital.models import Admision
from users.mixins import LoginRequiredMixin


class ContratoPermissionMixin(PermissionRequiredMixin):
    permission_required = 'contracts.contrato'


class IndexView(LoginRequiredMixin, TemplateView, ContratoPermissionMixin):
    template_name = 'contracts/index.html'

    def create_forms(self, context):
        context['vendedor-search'] = VendedorChoiceForm(
            prefix='vendedor-search')
        context['vendedor-search'].helper.form_action = 'vendedor-search'
        context['plan-search'] = PlanChoiceForm(prefix='plan-search')
        context['plan-search'].helper.form_action = 'plan-search'

        context['contrato-periodo'] = PeriodoForm(prefix='contrato-periodo')
        context['contrato-periodo'].set_legend('Contratos de un Periodo')
        context['contrato-periodo'].helper.form_action = 'contrato-periodo'

        context['evento-periodo'] = PeriodoForm(prefix='evento-periodo')
        context['evento-periodo'].set_legend('Eventos de un Periodo')
        context['evento-periodo'].helper.form_action = 'evento-periodo'

        context['vendedor-periodo'] = VendedorPeriodoForm(
            prefix='vendedor-periodo')
        context['vendedor-periodo'].helper.form_action = 'vendedor-periodo'

        context['contrato-search'] = ContratoSearchForm(
            prefix='contrato-search')
        context['contrato-search'].helper.form_action = 'contrato-search'
        context['contrato-persona-search'] = PersonaSearchForm(
            prefix='contrato-persona-search')
        context[
            'contrato-persona-search'].helper.form_action = \
            'contrato-persona-search'

        context['empresa-search'] = EmpleadorChoiceForm(prefix='empresa-search')
        context['empresa-search'].helper.form_action = 'empresa-search'

    def get_fechas(self):
        self.fin, self.inicio = get_current_month_range()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        self.get_fechas()
        self.create_forms(context)
        contratos = Contrato.objects.filter(inicio__gte=self.inicio,
                                            inicio__lte=self.fin)
        context['vendedores'] = Vendedor.objects.filter(habilitado=True).all()

        privados = Contrato.objects.filter(inicio__gte=self.inicio,
                                           cancelado=False).all()
        empresariales = Contrato.objects.filter(inicio__gte=self.inicio,
                                                cancelado=False).all()

        context['consulta'] = Consulta.objects.filter(created__gte=self.inicio,
                                                      created__lte=self.fin).count()
        context['seguimientos'] = Seguimiento.objects.filter(
            created__gte=self.inicio,
            created__lte=self.fin).count()

        # TODO Optimize using a map or a process pool
        personas = Persona.objects.filter(contratos__in=privados)
        context['citas'] = Cita.objects.filter(
            fecha__gte=self.inicio,
            fecha__lte=self.fin,
            persona__in=personas).count()

        personas = Persona.objects.filter(contratos__in=empresariales)

        context['citasp'] = Cita.objects.filter(
            fecha__gte=self.inicio,
            fecha__lte=self.fin,
            persona__in=personas).count()

        context['consultasp'] = Consulta.objects.filter(
            created__gte=self.inicio,
            created__lte=self.fin,
            persona__in=personas).count()

        morosos = Contrato.objects.filter(vencimiento__gte=self.fin,
                                          cancelado=False).all()
        context['mora'] = morosos.count()

        context['ingresos'] = Contrato.objects.filter(
            cancelado=False).aggregate(Sum('plan__precio'))

        context['contratos'] = contratos.count()
        context['meta'] = Meta.objects.last()
        context['cancelaciones'] = Cancelacion.objects.filter(
            fecha__gte=self.inicio).count()
        # TODO Hospitalizaciones y cirugias empresariales
        contratos_e = Contrato.objects.filter(inicio__gte=self.inicio,
                                              inicio__lte=self.fin)
        context['contratos_empresariales'] = contratos_e.count()
        context['hospitalizaciones'] = Admision.objects.filter(
            ingreso__gte=self.inicio).count()
        context['empresas'] = Empleador.objects.all()
        context['ingresos_empresa'] = Contrato.objects.filter(
            cancelado=False).aggregate(Sum('plan__precio'))
        morosos = Contrato.objects.filter(vencimiento__lte=self.fin).all()
        context['mora_empresa'] = morosos.count()

        context['cancelaciones_empresa'] = Cancelacion.objects.filter(
            fecha__gte=self.inicio).count()

        context['planes'] = Plan.objects.all()

        context['aseguradoras'] = Aseguradora.objects.all()

        return context


class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm


class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm


class PlanDetailView(LoginRequiredMixin, DetailView):
    model = Plan
    context_object_name = 'plan'


class PlanListView(LoginRequiredMixin, ListView):
    model = Plan
    context_object_name = 'planes'


class PlanCloneView(LoginRequiredMixin, RedirectView):
    """Allows cloning :class:`Plan` and its related member"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        plan = get_object_or_404(Plan, pk=kwargs['pk'])
        plan.pk = None
        plan.save()
        clone = plan

        plan = get_object_or_404(Plan, pk=kwargs['pk'])

        for beneficio in plan.beneficios.all():
            beneficio.plan = clone
            beneficio.pk = None
            beneficio.save()

        messages.info(self.request, _('¡Plan Copiado Exitosamente!'))
        return plan.get_absolute_url()


class PlanMixin(ContextMixin, View):
    def dispatch(self, *args, **kwargs):
        self.plan = get_object_or_404(Plan, pk=kwargs['plan'])
        return super(PlanMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlanMixin, self).get_context_data(**kwargs)
        context['plan'] = self.plan
        return context


class PlanFormMixin(PlanMixin, FormMixin):
    def get_initial(self):
        initial = super(PlanFormMixin, self).get_initial()
        initial = initial.copy()
        initial['plan'] = self.plan.id
        return initial


class PlanSearchView(LoginRequiredMixin, FormView):
    form_class = PlanChoiceForm
    prefix = 'plan-search'

    def form_valid(self, form):
        self.plan = form.cleaned_data['plan']
        return super(PlanSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.plan.get_absolute_url()


class BeneficioCreateView(LoginRequiredMixin, PlanFormMixin, CreateView):
    model = Beneficio
    form_class = BeneficioForm


class BeneficioUpdateView(LoginRequiredMixin, UpdateView):
    model = Beneficio
    form_class = BeneficioForm


class EmpresaSearchView(LoginRequiredMixin, FormView):
    form_class = EmpleadorChoiceForm
    prefix = 'empleador-search'
    template_name = 'contracts/empresa_form.html'

    def form_valid(self, form):
        self.empresa = form.cleaned_data['empresa']
        return super(EmpresaSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.empresa.get_absolute_url()


class LimiteEventoCreateView(LoginRequiredMixin, PlanFormMixin, CreateView):
    model = LimiteEvento
    form_class = LimiteEventoForm


class ContratoFormMixin(FormMixin, View):
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


class ContratoCreateView(LoginRequiredMixin, PersonaFormMixin, CreateView):
    model = Contrato
    form_class = ContratoForm


class ContratoEmpresarialCreateView(ContratoCreateView):
    form_class = ContratoEmpresarialForm


class ContratoPersonaCreateView(LoginRequiredMixin, CreateView):
    model = Contrato
    template_name = 'contracts/contrato_create.html'

    def dispatch(self, request, *args, **kwargs):

        self.persona = Persona()

        self.ContratoFormset = inlineformset_factory(Persona, Contrato,
                                                     form=ContratoForm,
                                                     fk_name='persona', extra=1)
        return super(ContratoPersonaCreateView, self).dispatch(request, *args,
                                                               **kwargs)

    def get_form(self, form_class=None):
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

        return self.contrato.get_absolute_url()


class ContratoMasterPersonaCreateView(LoginRequiredMixin, PersonaFormMixin,
                                      CreateView):
    model = Contrato
    form_class = ContratoMasterForm
    template_name = 'contracts/contrato_master_create.html'

    def form_valid(self, form):
        master = form.cleaned_data['master']
        self.object = master.create_contract(form.cleaned_data['persona'],
                                             form.cleaned_data['vencimiento'],
                                             form.cleaned_data['certificado'],
                                             0, True)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ContratoDetailView(LoginRequiredMixin, SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = 'contracts/contrato_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['contrato'] = self.object
        return super(ContratoDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Contrato.objects.all())
        return self.object.beneficiarios.select_related('persona').all()


class ContratoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    context_object_name = 'contrato'


class ContratoBeneficiarioListView(LoginRequiredMixin, ListView):
    model = Contrato
    context_object_name = 'contratos'
    template_name = 'contracts/contrato_beneficiarios_list.html'


class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    context_object_name = 'contratos'

    def get_queryset(self):
        return Contrato.objects.filter(
            cancelado=False,
            vencimiento__gte=timezone.now()
        ).all()

    def get_context_data(self, **kwargs):
        """Calculates the total morarorium and makes it available to the
        template"""

        context = super(ContratoListView, self).get_context_data(**kwargs)

        contratos = self.get_queryset()
        context['morosos'] = len([c for c in contratos if c.dias_mora() > 0])
        if contratos.count() > 0:
            context['percentage'] = context['morosos'] / float(
                contratos.count()) * 100

        return context


class ContratoEmpresarialListView(LoginRequiredMixin, ListView):
    model = Contrato
    context_object_name = 'contratos'

    def get_queryset(self):
        return Contrato.objects.filter(
            cancelado=False,
            vencimiento__gte=timezone.now()
        ).all()


class ContratoPeriodoView(LoginRequiredMixin, TemplateView):
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


class ContratoSearchView(LoginRequiredMixin, FormView):
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


class PagoDeleteView(LoginRequiredMixin, DeleteView):
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


class PagoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pago
    form_class = PagoForm


class EventoCreateView(ContratoFormMixin):
    model = Evento
    form_class = EventoForm


class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm


class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento

    def get_object(self, queryset=None):
        obj = super(EventoDeleteView, self).get_object(queryset)
        self.contrato = obj.contrato
        return obj

    def get_success_url(self):
        return self.contrato.get_absolute_url()


class EventoPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra los :class:`Evento`s de un periodo"""
    template_name = 'contracts/periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm(request.GET, prefix='evento-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.eventos = Evento.objects.filter(
                fecha__gte=self.inicio,
                fecha__lte=self.fin,
            )
        return super(EventoPeriodoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventoPeriodoView, self).get_context_data(**kwargs)

        context['contratos'] = self.contratos
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context


class VendedorCreateView(LoginRequiredMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm


class VendedorDetailView(LoginRequiredMixin, DetailView):
    model = Vendedor
    context_object_name = 'vendedor'


class VendedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm


class VendedorSearchView(LoginRequiredMixin, FormView):
    form_class = VendedorChoiceForm
    prefix = 'vendedor-search'

    def form_valid(self, form):
        self.vendedor = form.cleaned_data['vendedor']
        return super(VendedorSearchView, self).form_valid(form)

    def get_success_url(self):
        return self.vendedor.get_absolute_url()


class VendedorPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra los contratos de un periodo"""
    template_name = 'contracts/periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = VendedorPeriodoForm(request.GET, prefix='vendedor-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            vendedor = self.form.cleaned_data['vendedor']
            self.contratos = Contrato.objects.filter(
                inicio__gte=self.inicio,
                inicio__lte=self.fin,
                vendedor=vendedor,
            )
        return super(VendedorPeriodoView, self).dispatch(request, *args,
                                                         **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VendedorPeriodoView, self).get_context_data(**kwargs)

        context['contratos'] = self.contratos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['comision'] = \
            self.contratos.aggregate(total=Sum('plan__comision'))['total']

        return context


class TipoEventoCreateView(LoginRequiredMixin, CreateView):
    model = TipoEvento
    form_class = TipoEventoForm


class BeneficiarioCreateView(LoginRequiredMixin, PersonaFormMixin, CreateView):
    model = Beneficiario
    form_class = BeneficiarioPersonaForm


class BeneficiarioPersonaCreateView(LoginRequiredMixin, ContratoFormMixin,
                                    TemplateView):
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

    def get_form(self, form_class=None):
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


class BeneficiarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Beneficiario

    def get_object(self, queryset=None):
        obj = super(BeneficiarioDeleteView, self).get_object(queryset)
        self.contrato = obj.contrato
        return obj

    def get_success_url(self):
        return self.contrato.get_absolute_url()


class ContratoPersonaSearchView(LoginRequiredMixin, ListView):
    context_object_name = 'contratos'
    model = Contrato
    template_name = 'contracts/contrato_list.html'

    def get_queryset(self):
        form = PersonaSearchForm(self.request.GET,
                                 prefix='contrato-persona-search')
        form.is_valid()

        query = form.cleaned_data['query']

        queryset = Contrato.objects.filter(
            Q(persona__nombre__icontains=query) |
            Q(persona__apellido__icontains=query) |
            Q(persona__identificacion__icontains=query)
        )

        return queryset.all()


class MetaCreateView(LoginRequiredMixin, CreateView):
    model = Meta
    form_class = MetaForm


class MetaUpdateView(LoginRequiredMixin, UpdateView):
    model = Meta
    form_class = MetaForm


class MetaDetailView(LoginRequiredMixin, DetailView):
    model = Meta
    context_object_name = 'meta'


class CancelacionCreateView(LoginRequiredMixin, ContratoFormMixin, CreateView):
    model = Cancelacion
    form_class = CancelacionForm

    def form_valid(self, form):
        """Ademas de registrar la """

        self.object = form.save(commit=False)
        self.object.contrato.cancelado = True
        self.object.save()
        self.object.contrato.save()

        return HttpResponseRedirect(self.get_success_url())


class PrecontratoInline(InlineFormSet):
    model = Precontrato
    form_class = PrecontratoForm
    can_delete = False
    extra = 1


class PrecontratoCreateView(CreateWithInlinesView):
    model = Persona
    form_class = PersonaPrecontratoForm
    template_name = 'contracts/precontrato_create.html'
    inlines = [PrecontratoInline, ]

    def get_success_url(self):
        precontrato = self.object.precontratos.first()

        url = self.request.build_absolute_uri(precontrato.get_absolute_url())

        # TODO: Send email containing the URL

        return precontrato.get_absolute_url()


class PrecontratoDetailView(DetailView):
    model = Precontrato
    context_object_name = 'precontrato'


class PrecontratoMixin(View):
    def dispatch(self, *args, **kwargs):
        self.precontrato = get_object_or_404(Precontrato, pk=kwargs['pk'])
        return super(PrecontratoMixin, self).dispatch(*args, **kwargs)


class PrebeneficiarioCreateView(PrecontratoMixin, CreateView):
    model = Persona
    form_class = ButtonPersonaForm

    def form_valid(self, form):
        """Ademas de registrar la """

        persona = form.save(commit=False)
        prebeneficiaro = Prebeneficiario(persona=persona,
                                         precontrato=self.precontrato)

        return HttpResponseRedirect(prebeneficiaro.get_absolute_url())


class MasterContractDetailView(LoginRequiredMixin, DetailView):
    model = MasterContract
    context_object_name = 'master_contract'


class MasterContractCreateView(LoginRequiredMixin, CreateView):
    model = MasterContract
    form_class = MasterContractForm


class MasterContractUpdateView(LoginRequiredMixin, UpdateView):
    model = MasterContract
    form_class = MasterContractForm

    def form_valid(self, form):
        """Ademas de registrar la """

        self.object = form.save()

        for contrato in self.object.contratos.all():
            contrato.plan = self.object.plan
            contrato.save()

        return HttpResponseRedirect(self.get_success_url())


class MasterContractListView(LoginRequiredMixin, ListView):
    model = MasterContract
    context_object_name = 'contratos'


class MasterContractProcessView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        master = get_object_or_404(MasterContract, pk=kwargs['pk'])
        master.assign_contracts()

        messages.info(self.request, _('¡Creados los contratos!'))
        return master.get_absolute_url()


class ImportFileCreateView(LoginRequiredMixin, CreateView):
    model = ImportFile
    form_class = ImportFileForm


class ImportFileDetailView(LoginRequiredMixin, DetailView):
    model = ImportFile
    context_object_name = 'import_file'


class ImportFileProcessView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        import_file = get_object_or_404(ImportFile, pk=kwargs['pk'])
        import_file.assign_contracts()

        messages.info(self.request, _('¡Archivo Importado Exitosamente!'))
        return import_file.get_absolute_url()


class ImportFileListView(LoginRequiredMixin, ListView):
    model = ImportFile
    context_object_name = 'files'


class PCDUpdateView(LoginRequiredMixin, UpdateView):
    model = PCD
    form_class = PCDForm


class AseguradoraCreateView(LoginRequiredMixin, CreateView):
    model = Aseguradora
    form_class = AseguradoraForm


class AseguradoraDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the Data corresponding to the :class:`Aseguradora`
    """
    model = Aseguradora
    context_object_name = 'aseguradora'

    def get_context_data(self, **kwargs):
        """
        Adds statistical data concerning to the :class:`Aseguradora` displayed
        in UI.
        """
        context = super(AseguradoraDetailView, self).get_context_data(**kwargs)

        meses = []
        now = timezone.now()

        forms = []

        for n in range(1, 13):
            start = now.replace(month=n, day=1)
            inicio, fin = make_month_range(start)

            form = AseguradoraPeriodoForm(initial={
                'aseguradora': self.object,
                'inicio': inicio,
                'fin': fin,
            })

            form.set_action('contracts-aseguradora-mensual')
            form.helper.attrs = {'target': '_blank'}
            form.helper.layout = Layout()
            form.fields['inicio'].widget = HiddenInput()
            form.fields['fin'].widget = HiddenInput()
            form.fields['aseguradora'].widget = HiddenInput()
            form.helper.form_method = 'get'
            form.helper.add_input(Submit(
                'submit',
                _('{0}'.format(calendar.month_name[n])),
                css_class='btn-block'
            ))

            form.helper.form_class = ''
            form.helper.label_class = ''
            form.helper.field_class = ''

            forms.append(form)

            consultas = Consulta.objects.atendidas(inicio, fin).filter(
                contrato__master__aseguradora=self.object
            )
            quejas = Queja.objects.filter(
                created__range=(inicio, fin),
                respuesta__consulta__contrato__master__aseguradora=self.object,
            ).count()

            satisfaccion = Voto.objects.filter(
                opcion__isnull=False,
                created__range=(inicio, fin),
                pregunta__calificable=True,
                respuesta__consulta__poliza__aseguradora=self.object,
            ).aggregate(average=Coalesce(Avg('opcion__valor'), 0))['average']

            incapacidades = Incapacidad.objects.filter(
                consulta__contrato__master__aseguradora=self.object,
                consulta__created__range=(inicio, fin)
            )

            total_incapacidades = incapacidades.aggregate(
                total=Coalesce(Sum('dias'), 0)
            )['total']

            diurnas = consultas.filter(
                created__hour__range=(7, 19)
            ).count()

            nocturnas = consultas.exclude(
                created__hour__range=(7, 19)
            ).count()

            meses.append({
                'inicio': inicio,
                'fin': fin,
                'consultas': consultas.count(),
                'diurnas': diurnas,
                'nocturnas': nocturnas,
                'quejas': quejas,
                'satisfaccion': satisfaccion,
                'incapacidades': incapacidades.count(),
                'total_incapacidades': total_incapacidades,
            })

        context['meses'] = meses
        context['forms'] = forms

        return context


class AseguradoraUpdateView(LoginRequiredMixin, UpdateView):
    model = Aseguradora
    form_class = AseguradoraForm


class AseguradoraMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.aseguradora = get_object_or_404(Aseguradora,
                                             pk=kwargs['aseguradora'])
        return super(AseguradoraMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AseguradoraMixin, self).get_context_data(**kwargs)

        context['aseguradora'] = self.aseguradora

        return context


class AseguradoraPeriodoView(LoginRequiredMixin, TemplateView):
    """
    Shows the monthly data related to a :class:`Aseguradora`
    """
    template_name = 'contracts/aseguradora_month.html'

    def dispatch(self, request, *args, **kwargs):

        form = AseguradoraPeriodoForm(request.GET)

        if form.is_valid():
            self.inicio = form.cleaned_data['inicio']
            self.fin = form.cleaned_data['fin']
            self.aseguradora = form.cleaned_data['aseguradora']
        else:
            messages.info(
                self.request,
                _('Los Datos Ingresados en el formulario no son válidos')
            )
            return HttpResponseRedirect(reverse('contracts-index'))

        return super(AseguradoraPeriodoView, self).dispatch(request, *args,
                                                            **kwargs)

    def get_context_data(self, **kwargs):
        """
        Builds the data that will be displayed in the GUI
        """
        context = super(AseguradoraPeriodoView, self).get_context_data(**kwargs)
        context['aseguradora'] = self.aseguradora
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        inicio = self.inicio
        fin = self.fin

        context['ventas'] = Venta.objects.periodo(inicio, fin).filter(
            recibo__cliente__contratos__master__aseguradora=self.aseguradora,
        ).values(
            'item__item_type__nombre',
        ).annotate(
            count=Count('id')
        ).order_by('count')
        context['consultas'] = Consulta.objects.atendidas(inicio, fin).filter(
            contrato__master__aseguradora=self.aseguradora,
        )

        context['quejas'] = Queja.objects.filter(
            created__range=(inicio, fin),
            respuesta__consulta__contrato__master__aseguradora=self.aseguradora,
        )

        context['satisfaccion'] = Voto.objects.filter(
            opcion__isnull=False,
            created__range=(inicio, fin),
            pregunta__calificable=True,
            respuesta__consulta__poliza__aseguradora=self.aseguradora,
        ).aggregate(average=Coalesce(Avg('opcion__valor'), 0))['average']

        return context
