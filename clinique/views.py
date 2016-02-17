# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
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

from collections import defaultdict
from datetime import time, timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, CreateView, View, ListView, \
    UpdateView, TemplateView, RedirectView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from clinique.forms import CitaForm, EvaluacionForm, \
    ConsultaForm, SeguimientoForm, LecturaSignosForm, DiagnosticoClinicoForm, \
    ConsultorioForm, CitaPersonaForm, CargoForm, OrdenMedicaForm, \
    NotaEnfermeriaForm, ExamenForm, EsperaForm, PacienteSearchForm, \
    PrescripcionForm, IncapacidadForm, ReporteForm, RemisionForm, \
    PrescripcionFormSet, NotaMedicaForm, ConsultaEsperaForm, \
    EsperaConsultorioForm
from clinique.models import Cita, Consulta, Evaluacion, Seguimiento, \
    LecturaSignos, Consultorio, DiagnosticoClinico, Cargo, OrdenMedica, \
    NotaEnfermeria, Examen, Espera, Prescripcion, Incapacidad, Reporte, \
    Remision, \
    NotaMedica
from contracts.models import MasterContract
from emergency.models import Emergencia
from hospinet.utils import get_current_month_range
from inventory.models import ItemTemplate, TipoVenta
from inventory.views import UserInventarioRequiredMixin
from invoice.forms import PeriodoForm
from persona.forms import FisicoForm, AntecedenteForm, PersonaForm, \
    AntecedenteFamiliarForm, AntecedenteObstetricoForm, EstiloVidaForm, \
    AntecedenteQuirurgicoForm
from persona.models import Fisico, Antecedente, AntecedenteFamiliar, \
    AntecedenteObstetrico, AntecedenteQuirurgico, EstiloVida, Persona
from persona.views import PersonaFormMixin, AntecedenteObstetricoCreateView
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class ConsultorioPermissionMixin(LoginRequiredMixin):
    @method_decorator(permission_required('clinique.consultorio'))
    def dispatch(self, *args, **kwargs):
        return super(ConsultorioPermissionMixin, self).dispatch(*args, **kwargs)


class DateBoundView(View):
    def dispatch(self, request, *args, **kwargs):
        tz = timezone.get_current_timezone()
        now = timezone.now()
        day = timedelta(days=1)
        self.yesterday = now - day
        self.today = tz.localize(datetime.combine(now, time.min))
        self.fin, self.inicio = get_current_month_range()

        return super(DateBoundView, self).dispatch(request, *args, **kwargs)


class ConsultorioIndexView(ConsultorioPermissionMixin, DateBoundView, ListView):
    template_name = 'clinique/index.html'
    paginate_by = 20
    context_object_name = 'pacientes'
    model = Consultorio
    queryset = Consultorio.objects.select_related(
            'usuario',
            'secretaria',
    )

    def get_context_data(self, **kwargs):
        context = super(ConsultorioIndexView, self).get_context_data(**kwargs)
        context['citaperiodoform'] = PeriodoForm(prefix='cita-periodo')
        context['citaperiodoform'].helper.form_action = 'cita-periodo'
        context['citaperiodoform'].set_legend(_('Citas por Periodo'))

        context['diagnosticoperiodoform'] = PeriodoForm(
                prefix='diagnostico-periodo')
        context[
            'diagnosticoperiodoform'].helper.form_action = 'diagnostico-periodo'
        context['diagnosticoperiodoform'].set_legend(
                _('Diagnosticos por Periodo'))

        context['cargosperiodoform'] = PeriodoForm(prefix='cargo-periodo')
        context['cargosperiodoform'].helper.form_action = 'cargo-periodo'
        context['cargosperiodoform'].set_legend(_('Cargos por Periodo'))

        context['consultasperiodoform'] = PeriodoForm(prefix='consulta')
        context['consultasperiodoform'].helper.form_action = 'consulta-periodo'
        context['consultasperiodoform'].set_legend(_('Consultas por Periodo'))

        context['evaluacionperiodoform'] = PeriodoForm(
                prefix='evaluacion-periodo')
        context[
            'evaluacionperiodoform'].helper.form_action = 'evaluacion-periodo'
        context['evaluacionperiodoform'].set_legend(
                _('Evaluaciones por Periodo')
        )

        context['seguimientoperiodoform'] = PeriodoForm(
                prefix='seguimiento-periodo')
        context[
            'seguimientoperiodoform'].helper.form_action = 'seguimiento-periodo'
        context['seguimientoperiodoform'].set_legend(
                _('Seguimientos por Periodo')
        )

        context['pacientesearch'] = PacienteSearchForm()
        context[
            'pacientesearch'].helper.form_action = \
            'clinique-paciente-search-add'

        context['esperas'] = Espera.objects.filter(
                fecha__gte=self.yesterday,
                consulta=False,
                terminada=False,
                atendido=False,
                ausente=False
        ).select_related(
                'persona',
                'consultorio',
                'consultorio__usuario',
                'consultorio__secretaria',
        ).all()

        context['consulta_estadistica'] = PeriodoForm(
                prefix='consulta-estadistica'
        )

        context[
            'consulta_estadistica'].helper.form_action = 'consulta-estadisticas'
        context['consulta_estadistica'].set_legend(
                _('Estad&iacute;sticas de Consulta')
        )

        return context


class ConsultorioDetailView(LoginRequiredMixin, DateBoundView,
                            SingleObjectMixin, ListView):
    paginate_by = 20
    template_name = 'clinique/consultorio_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ConsultorioDetailView, self).get_context_data(**kwargs)

        context['consultorio'] = self.object
        context['buscar'] = PacienteSearchForm(
                initial={'consultorio': self.object.id})

        context['total'] = sum(e.tiempo() for e in self.get_queryset().all())
        context['citas'] = Cita.objects.filter(consultorio=self.object,
                                               fecha__gte=self.yesterday,
                                               fecha__lte=self.fin,
                                               ausente=False, atendida=False)

        context['consultas'] = Espera.objects.filter(consultorio=self.object,
                                                     consulta=True,
                                                     terminada=False)

        return context

    def get_queryset(self):
        self.object = self.get_object(Consultorio.objects.all())
        queryset = self.object.espera.filter(fecha__gte=self.yesterday,
                                             consulta=False, terminada=False,
                                             atendido=False, ausente=False)
        return queryset


class ConsultorioCreateView(CurrentUserFormMixin, CreateView):
    model = Consultorio
    form_class = ConsultorioForm


class ConsultorioMixin(View):
    def dispatch(self, *args, **kwargs):
        self.consultorio = get_object_or_404(Consultorio,
                                             pk=kwargs['consultorio'])
        return super(ConsultorioMixin, self).dispatch(*args, **kwargs)


class ConsultorioFormMixin(ConsultorioMixin):
    def get_initial(self):
        initial = super(ConsultorioFormMixin, self).get_initial()
        initial['consultorio'] = self.consultorio.id
        return initial


class PacienteDetailView(LoginRequiredMixin, DetailView):
    """Permite ver los datos del :class"`Paciente` en la interfaz gráfica"""

    model = Persona
    context_object_name = 'paciente'
    template_name = 'clinique/paciente_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PacienteDetailView, self).get_context_data()

        context['consultas'] = self.object.consultas.filter(facturada=False,
                                                            activa=True).all()

        return context


class ConsultaMixin(ContextMixin):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])
        return super(ConsultaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConsultaMixin, self).get_context_data(**kwargs)

        context['consulta'] = self.consulta

        return context


class ConsultaFormMixin(ConsultaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(ConsultaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['consulta'] = self.consulta
        return initial


class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm


class CitaPersonaCreateView(LoginRequiredMixin, CreateView, PersonaFormMixin):
    model = Cita
    form_class = CitaPersonaForm


class CitaPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra los contratos de un periodo"""
    template_name = 'clinique/cita_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm(request.GET, prefix='cita-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.citas = Cita.objects.filter(
                    fecha__gte=self.inicio,
                    fecha__lte=self.fin
            )
        return super(CitaPeriodoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CitaPeriodoView, self).get_context_data(**kwargs)

        context['citas'] = self.citas
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context


class DiagnosticoPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra los :class:`DiagnosticoClinico` de un periodo"""
    template_name = 'clinique/diagnostico_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm(request.GET, prefix='diagnostico-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.diagnosticos = DiagnosticoClinico.objects.filter(
                    created__gte=self.inicio,
                    created__lte=self.fin
            ).order_by('consulta__consultorio')
        return super(DiagnosticoPeriodoView, self).dispatch(request, *args,
                                                            **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiagnosticoPeriodoView, self).get_context_data(**kwargs)

        context['diagnosticos'] = self.diagnosticos
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        context['total'] = self.diagnosticos.count()

        DiagnosticoClinico.objects.values('consulta__consultorio').annotate(
                consultorio_count=Count('consulta__consultorio')
        ).filter(created__gte=self.inicio, created__lte=self.fin)

        cons = defaultdict(int)
        consultorios = Consultorio.objects.all()
        for consultorio in consultorios:
            cons[consultorio] = DiagnosticoClinico.objects.filter(
                    created__gte=self.inicio, created__lte=self.fin,
                    consulta__consultorio=consultorio).count()

        cons = dict((k, v) for k, v in cons.items() if v > 0)

        context['consultorios'] = reversed(
                sorted(cons.iteritems(), key=lambda x: x[1]))
        context['consultorio_graph'] = reversed(
                sorted(cons.iteritems(), key=lambda x: x[1]))
        context['consultorio_graph2'] = reversed(
                sorted(cons.iteritems(), key=lambda x: x[1]))

        return context


class CargoPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra los :class:`Cargo` de un periodo"""
    template_name = 'clinique/cargo_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm(request.GET, prefix='cargo-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.cargos = Cargo.objects.filter(
                    created__gte=self.inicio,
                    created__lte=self.fin
            )
        return super(CargoPeriodoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CargoPeriodoView, self).get_context_data(**kwargs)

        context['cargos'] = self.cargos
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        context['cuenta'] = ItemTemplate.objects.values('descripcion').annotate(
                cargo_count=Count('consultorio_cargos')).filter(
                consultorio_cargos__created__gte=self.inicio,
                consultorio_cargos__created__lte=self.fin)

        return context


class CitaListView(LoginRequiredMixin, ConsultorioMixin, ListView):
    model = Cita
    context_object_name = 'citas'

    def get_queryset(self):
        self.citas = Cita.objects.filter(consultorio=self.consultorio,
                                         fecha__gte=timezone.now().date(),
                                         ausente=False)

        return self.citas.all()

    def get_context_data(self, **kwargs):
        context = super(CitaListView, self).get_context_data(**kwargs)
        context['consultorio'] = self.consultorio

        fechas = defaultdict(list)

        for cita in self.citas.all():
            fechas[cita.fecha.date()].append(cita)

        context['fechas'] = fechas.iteritems()
        return context


class CitaAusenteView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        cita = get_object_or_404(Cita, pk=kwargs['pk'])
        cita.ausente = True
        cita.save()
        messages.info(
                self.request,
                _('¡Se marco la espera como ausente!')
        )
        return cita.get_absolute_url()


class EvaluacionCreateView(CurrentUserFormMixin, ConsultaFormMixin,
                           PersonaFormMixin, CreateView):
    model = Evaluacion
    form_class = EvaluacionForm


class EvaluacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Evaluacion
    form_class = EvaluacionForm


class EvaluacionPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra los :class:`Evaluacion` de un periodo"""
    template_name = 'clinique/evaluacion_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm(request.GET, prefix='evaluacion-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.evaluaciones = Evaluacion.objects.filter(
                    created__gte=self.inicio,
                    created__lte=self.fin
            ).order_by('paciente__consultorio')
        return super(EvaluacionPeriodoView, self).dispatch(request, *args,
                                                           **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EvaluacionPeriodoView, self).get_context_data(**kwargs)

        context['evaluaciones'] = self.evaluaciones
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        return context


class EsperaMixin(object):
    """
    Populates a :class:`Espera` with data comming from the url
    """

    def dispatch(self, *args, **kwargs):
        self.espera = get_object_or_404(Espera, pk=kwargs['espera'])
        return super(EsperaMixin, self).dispatch(*args, **kwargs)


class EsperaFormMixin(EsperaMixin, FormMixin):
    """
    Adds a :class:`Espera` data to a form initial arguments
    """

    def get_initial(self):
        initial = super(EsperaFormMixin, self).get_initial()
        initial['espera'] = self.espera
        return initial


class ConsultaEsperaCreateView(CurrentUserFormMixin, EsperaFormMixin,
                               CreateView):
    """
    Creates a :class:`Consulta` based in a :class:`Espera` data
    """
    model = Consulta
    form_class = ConsultaEsperaForm

    def get_initial(self):
        initial = super(ConsultaEsperaCreateView, self).get_initial()
        initial['persona'] = self.espera.persona
        initial['poliza'] = self.espera.poliza
        initial['consultorio'] = self.espera.consultorio
        return initial


def get_active_master_contracts(persona):
    """
    Builds a :class:`QuerySet` that searches the :class:`MasterContract`s
    associated to all active :class:`Contract` of a :class:`Persona`
    :param persona: The :class:`Persona` that will be used to obtain
                    :class:`MasterContract`:s
    :return: :class:`QuerySet`
    """
    queryset = None
    if persona.contratos.filter(
            vencimiento__gte=timezone.now()
    ).count() >= 1:
        masters = persona.contratos.filter(
                vencimiento__gte=timezone.now()
        ).values('master')
        masters = [master['master'] for master in masters]
        queryset = MasterContract.objects.select_related(
                'aseguradora',
                'plan',
                'contratante'
        ).filter(pk__in=masters)
    elif persona.beneficiarios.filter(
            contrato__vencimiento__gte=timezone.now()
    ).count() >= 1:
        masters = persona.beneficiarios.filter(
                contrato__vencimiento__gte=timezone.now()
        ).values('contrato__master')
        masters = [master['contrato__master'] for master in masters]
        queryset = MasterContract.objects.select_related(
                'aseguradora',
                'plan',
                'contratante'
        ).filter(pk__in=masters)
    return queryset


class ConsultaCreateView(CurrentUserFormMixin, PersonaFormMixin,
                         ConsultorioFormMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm

    def get_form(self, form_class=None):
        """
        Builds a form that contains all :class:`MasterContract` from the
        :class:`Persona` that is getting a :class:`Consulta`
        :param form_class:
        :return: :class:`ConsultaForm` instance
        """
        form = super(ConsultaCreateView, self).get_form(form_class)
        queryset = get_active_master_contracts(self.persona)
        if queryset:
            form.fields['poliza'].queryset = queryset
        return form


class ConsultaDetailView(LoginRequiredMixin, DetailView):
    model = Consulta
    context_object_name = 'consulta'


class SeguimientoCreateView(CurrentUserFormMixin, PersonaFormMixin, CreateView):
    model = Seguimiento
    form_class = SeguimientoForm


class SeguimientoPeriodoView(TemplateView, LoginRequiredMixin):
    """Muestra los :class:`Seguimiento`s de un periodo"""
    template_name = 'clinique/seguimiento_periodo.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = PeriodoForm(request.GET, prefix='seguimiento-periodo')

        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = datetime.combine(self.form.cleaned_data['fin'], time.max)
            self.seguimiento = Seguimiento.objects.filter(
                    created__gte=self.inicio,
                    created__lte=self.fin
            )
        return super(SeguimientoPeriodoView, self).dispatch(request, *args,
                                                            **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SeguimientoPeriodoView, self).get_context_data(**kwargs)

        context['seguimientos'] = self.seguimiento
        context['inicio'] = self.inicio
        context['fin'] = self.fin

        context['cuenta'] = Seguimiento.objects.values(
                'paciente').annotate(
                seguimiento_count=Count('id'))

        return context


class LecturaSignosCreateView(LoginRequiredMixin, PersonaFormMixin, CreateView):
    model = LecturaSignos
    form_class = LecturaSignosForm

    def form_valid(self, form):
        self.object = form.save(commit=True)

        esperas = Espera.objects.filter(persona=self.object.persona,
                                        terminada=False)

        for espera in esperas.all():
            espera.fecha = timezone.now()

        return HttpResponseRedirect(self.get_success_url())


class LecturaSignosUpdateView(LoginRequiredMixin, UpdateView):
    model = LecturaSignos
    form_class = LecturaSignosForm


class DiagnosticoCreateView(CurrentUserFormMixin, PersonaFormMixin,
                            ConsultaFormMixin, CreateView):
    model = DiagnosticoClinico
    form_class = DiagnosticoClinicoForm


class DiagnosticoUpdateView(LoginRequiredMixin, UpdateView):
    model = DiagnosticoClinico
    form_class = DiagnosticoClinicoForm


class CliniquePersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'clinique/persona_update.html'

    def get_success_url(self):
        return reverse('clinique-fisico-editar', args=[self.object.id])


class CliniqueFisicoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permite actualizar los datos del :class:`Fisico` de una :class:`Persona`
    """

    model = Fisico
    form_class = FisicoForm
    template_name = 'clinique/fisico_update.html'

    def get_success_url(self):
        return reverse('clinique-antecedente-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteUpdateView(LoginRequiredMixin, UpdateView):
    """Permite actualizar los datos del :class:`Antecedente` de una
    :class:`Persona`"""

    model = Antecedente
    form_class = AntecedenteForm
    template_name = 'clinique/antecedente_update.html'

    def get_success_url(self):
        return reverse('clinique-antecedente-familiar-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteObstetricoCreateView(AntecedenteObstetricoCreateView):
    def get_success_url(self):
        return reverse('clinique-antecedente-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteFamiliarUpdateView(LoginRequiredMixin, UpdateView):
    """Permite actualizar los datos del :class:`AntecedenteFamiliar` de una
    :class:`Persona`"""

    model = AntecedenteFamiliar
    form_class = AntecedenteFamiliarForm
    template_name = 'clinique/antecedente_familiar_update.html'

    def get_success_url(self):
        return reverse('clinique-estilovida-editar',
                       args=[self.object.persona.id])


class CliniqueAntecedenteObstetricoUpdateView(LoginRequiredMixin, UpdateView):
    """Permite actualizar los datos del :class:`AntecedenteObstetrico` de una
    :class:`Persona`"""

    model = AntecedenteObstetrico
    form_class = AntecedenteObstetricoForm
    template_name = 'clinique/antecedente_obstetrico_update.html'


class CliniqueAntecedenteQuirurgicoUpdateView(LoginRequiredMixin, UpdateView):
    """Permite actualizar los datos del :class:`AntecedenteQuirurgico` de una
    :class:`Persona`"""

    model = AntecedenteQuirurgico
    form_class = AntecedenteQuirurgicoForm
    template_name = 'clinique/antecedente_quirurgico_update.html'

    def get_success_url(self):
        return reverse('clinique-antecedente-editar',
                       args=[self.object.persona.id])


class CliniqueEstiloVidaUpdateView(LoginRequiredMixin, UpdateView):
    """Permite actualizar los datos del :class:`EstiloVida` de una
    :class:`Persona`"""

    model = EstiloVida
    form_class = EstiloVidaForm
    template_name = 'clinique/estilo_vida_update.html'


class CargoCreateView(CurrentUserFormMixin, ConsultaFormMixin,
                      UserInventarioRequiredMixin, CreateView):
    """Permite crear :class:`Cargo`s durante una :class:`Consulta`"""
    model = Cargo
    form_class = CargoForm

    def form_valid(self, form):
        user = self.request.user
        if user.profile is None or user.profile.inventario is None:
            messages.info(self.request,
                          "Su usuario no tiene un Inventario asociado, por "
                          "favor edite su Perfil para asociar un Inventario")

            return redirect(self.request.META.get('HTTP_REFERER', '/'))

        self.object = form.save(commit=False)

        user.profile.inventario.descargar(self.object.item,
                                          self.object.cantidad,
                                          self.request.user)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class OrdenMedicaCreateView(CurrentUserFormMixin, ConsultaFormMixin,
                            CreateView):
    model = OrdenMedica
    form_class = OrdenMedicaForm


class OrdenMedicaUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenMedica
    form_class = OrdenMedicaForm


class OrdenMedicaDetailView(LoginRequiredMixin, DetailView):
    model = OrdenMedica
    context_object_name = 'orden'

    def get_context_data(self, **kwargs):
        context = super(OrdenMedicaDetailView, self).get_context_data(**kwargs)

        formset = PrescripcionFormSet(instance=self.object)
        context['formset'] = formset
        helper = FormHelper()
        helper.form_action = reverse('prescripcion-guardar',
                                     args=[self.object.id])
        helper.add_input(Submit('submit', _('Guardar')))
        context['helper'] = helper

        return context


class OrdenMedicaListView(LoginRequiredMixin, ListView):
    model = OrdenMedica
    context_object_name = 'ordenes'

    def get_queryset(self):
        return OrdenMedica.objects.filter(farmacia=False)


class OrdenCompletarRedirect(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        orden = get_object_or_404(OrdenMedica, pk=kwargs['pk'])
        orden.farmacia = True
        orden.save()

        return reverse('clinique-orden-list')


def save_prescriptions(request, orden):
    orden = get_object_or_404(OrdenMedica, pk=orden)
    if request.method == 'POST':
        formset = PrescripcionFormSet(request.POST, instance=orden)
        if formset.is_valid():
            formset.save()
            messages.info(request, _('Agregados los medicamentos'))

    return redirect(orden)


class NotaEnfermeriaCreateView(CurrentUserFormMixin, PersonaFormMixin,
                               CreateView):
    model = NotaEnfermeria
    form_class = NotaEnfermeriaForm


class ExamenCreateView(LoginRequiredMixin, PersonaFormMixin, CreateView):
    model = Examen
    form_class = ExamenForm


class ExamenUpdateView(LoginRequiredMixin, UpdateView):
    model = Examen
    form_class = ExamenForm


class EsperaCreateView(LoginRequiredMixin, PersonaFormMixin,
                       ConsultorioFormMixin, CreateView):
    model = Espera
    form_class = EsperaForm

    def get_form(self, form_class=None):
        """
        Builds a form that contains all :class:`MasterContract` from the
        :class:`Persona` that is getting a :class:`Consulta`
        :param form_class:
        :return: :class:`ConsultaForm` instance
        """
        form = super(EsperaCreateView, self).get_form(form_class)

        queryset = get_active_master_contracts(self.persona)
        if queryset:
            form.fields['poliza'].queryset = queryset
        return form


class EsperaUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows the user to change the :class:`Consultorio` for a :class:`Espera`
    """
    model = Espera
    form_class = EsperaConsultorioForm


class EsperaConsultorioCreateView(LoginRequiredMixin, PersonaFormMixin,
                                  CreateView):
    model = Espera
    form_class = EsperaForm

    def get_form(self, form_class=None):
        """
        Builds a form that contains all :class:`MasterContract` from the
        :class:`Persona` that is getting a :class:`Consulta`
        :param form_class:
        :return: :class:`ConsultaForm` instance
        """
        form = super(EsperaConsultorioCreateView, self).get_form(form_class)
        queryset = get_active_master_contracts(self.persona)
        if queryset:
            form.fields['poliza'].queryset = queryset
        return form


class EsperaListView(LoginRequiredMixin, ConsultorioMixin, ListView):
    model = Espera


class EsperaAusenteView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        espera = get_object_or_404(Espera, pk=kwargs['pk'])
        espera.ausente = True
        espera.fin = timezone.now()
        espera.save()
        messages.info(
                self.request,
                _('¡Se marco la espera como ausente!')
        )
        return espera.get_absolute_url()


class PrescripcionCreateView(CurrentUserFormMixin, PersonaFormMixin,
                             ConsultaFormMixin, CreateView):
    model = Prescripcion
    form_class = PrescripcionForm


class PrescripcionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescripcion
    form_class = PrescripcionForm


class IncapacidadCreateView(CurrentUserFormMixin, PersonaFormMixin,
                            ConsultaFormMixin, CreateView):
    model = Incapacidad
    form_class = IncapacidadForm


class IncapacidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Incapacidad
    form_class = IncapacidadForm


class IncapacidadListView(LoginRequiredMixin, ListView):
    model = Incapacidad
    context_object_name = 'incapacidades'


class ReporteCreateView(ConsultorioFormMixin, LoginRequiredMixin, CreateView):
    model = Reporte
    form_class = ReporteForm


class ReporteListView(LoginRequiredMixin, ListView):
    model = Reporte
    queryset = Reporte.objects.order_by('-created')
    context_object_name = 'reportes'
    paginate_by = 20


class CitaEsperaRedirectView(LoginRequiredMixin, RedirectView):
    """Crea una :class:´Espera´ a partir de una :class:´Cita´ y redirige al
    usuario al :class:´Consultorio´ asociado"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        cita = get_object_or_404(Cita, pk=kwargs['pk'])
        espera = cita.to_espera()
        espera.save()
        messages.info(
                self.request,
                _('¡Se envio el paciente a sala de espera!')
        )
        return espera.get_absolute_url()


class EsperaConsultaRedirectView(LoginRequiredMixin, RedirectView):
    """Crea una :class:´Espera´ a partir de una :class:´Cita´ y redirige al
    usuario al :class:´Consultorio´ asociado"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        espera = get_object_or_404(Espera, pk=kwargs['pk'])
        espera.consulta = True
        espera.fin = timezone.now()
        espera.save()
        messages.info(
                self.request,
                _('¡Se envio el paciente a consulta!')
        )
        return espera.get_absolute_url()


class EsperaTerminadaRedirectView(LoginRequiredMixin, RedirectView):
    """Marca una Espera como terminada y coloca como inactivas las consultas"""

    permanent = False

    def get_redirect_url(self, **kwargs):
        espera = get_object_or_404(Espera, pk=kwargs['pk'])
        espera.terminada = True

        for consulta in espera.consulta_set.all():
            consulta.activa = False
            consulta.save()

        espera.save()
        messages.info(
                self.request,
                _('¡La consulta se marcó como terminada!')
        )
        return espera.get_absolute_url()


class RemisionCreateView(LoginRequiredMixin, PersonaFormMixin, CreateView):
    """Permite crear una :class:`Remision` a una :class:`Persona`"""

    model = Remision
    form_class = RemisionForm


class ConsultaTerminadaRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        consulta = get_object_or_404(Consulta, pk=kwargs['pk'])
        consulta.activa = False
        consulta.final = timezone.now()
        consulta.save()
        if consulta.espera is not None:
            consulta.espera.terminada = True
            consulta.espera.save()
        else:
            Espera.objects.filter(
                    terminada=False, persona=consulta.persona
            ).update(
                    terminada=True
            )

        espera = Espera.objects.filter(
                consultorio__localidad=consulta.consultorio.localidad,
                terminada=False
        ).first()

        if espera is not None:
            espera.consulta = True
            espera.consultorio = consulta.consultorio
            espera.fin = timezone.now()
            espera.save()

        messages.info(
                self.request,
                _('¡La consulta se marcó como terminada!')
        )
        return consulta.get_absolute_url()


class ConsultaPeriodoView(LoginRequiredMixin, TemplateView):
    """Muestra las opciones disponibles para la aplicación"""

    template_name = 'clinique/consulta_list.html'

    def dispatch(self, request, *args, **kwargs):
        """Filtra las :class:`Emergencia` de acuerdo a los datos ingresados en
        el formulario"""

        self.form = PeriodoForm(request.GET, prefix='consulta')
        if self.form.is_valid():
            self.inicio = self.form.cleaned_data['inicio']
            self.fin = self.form.cleaned_data['fin']
            self.consultas = Consulta.objects.select_related(
                    'persona',
                    'tipo',
                    'consultorio',
                    'consultorio__usuario',
                    'consultorio__localidad',
            ).prefetch_related(
                    'cargos',
                    'cargos__item',
                    'diagnosticos_clinicos',
                    'diagnosticos_clinicos__afeccion',
                    'persona__contratos',
                    'persona__contratos__master__aseguradora',
                    'persona__contratos__beneficiarios',
                    'persona__beneficiarios',
                    'persona__beneficiarios__contrato',
            ).filter(
                    created__range=(self.inicio, self.fin)
            ).order_by('created')
        else:
            return redirect('invoice-index')

        return super(ConsultaPeriodoView, self).dispatch(request, *args,
                                                         **kwargs)

    def get_context_data(self, **kwargs):

        """Permite utilizar las :class:`Emergencia`s en la vista"""

        context = super(ConsultaPeriodoView, self).get_context_data(**kwargs)
        context['consultas'] = self.consultas
        context['inicio'] = self.inicio
        context['fin'] = self.fin
        return context


class ConsultaEstadisticaPeriodoListView(LoginRequiredMixin, ListView):
    """
    Shows a GUI with a list of :class:`Cheque that have been registered during
    the period of time indicated by a :class:`PeriodoForm`
    """
    model = Consulta
    context_object_name = 'consultas'
    template_name = 'clinique/consulta_estadistica.html'

    def get_queryset(self):
        """
        Filters the :class:`Consulta` objects
        :return: a filtered :class:`QuerySet`
        """
        form = PeriodoForm(self.request.GET, prefix='consulta-estadistica')
        if form.is_valid():
            self.inicio = form.cleaned_data['inicio']
            self.fin = form.cleaned_data['fin']
            return Consulta.objects.filter(
                    created__range=(
                        self.inicio,
                        self.fin
                    )
            ).select_related(
                    'consultorio',
                    'consultorio__usuario',
            ).order_by()
        return Consulta.objects.select_related(
                'consultorio',
                'consultorio__usuario',
        ).order_by()

    def get_context_data(self, **kwargs):
        context = super(ConsultaEstadisticaPeriodoListView,
                        self).get_context_data(**kwargs)

        context['inicio'] = self.inicio
        context['fin'] = self.fin

        context['medicos'] = self.get_queryset().values(
                'consultorio__usuario__first_name',
                'consultorio__usuario__last_name'
        ).annotate(
                consultas=Count('consultorio__usuario')
        )

        context['ciudades'] = self.get_queryset().values(
                'consultorio__localidad__nombre'
        ).annotate(
                consultas=Count('consultorio__localidad')
        )

        return context


class ConsultaRemitirView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        consulta = get_object_or_404(Consulta, pk=kwargs['pk'])
        consulta.remitida = True
        consulta.save()
        messages.info(
                self.request,
                _('¡Se remitio la consulta a especialista!')
        )
        return consulta.get_absolute_url()


class ConsultaRevisarView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        consulta = get_object_or_404(Consulta, pk=kwargs['pk'])
        consulta.revisada = True
        consulta.save()
        messages.info(self.request, _('¡La Consulta ha sido revisada!'))
        return consulta.get_absolute_url()


class ConsultaEmergenciaRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        consulta = get_object_or_404(Consulta, pk=kwargs['pk'])
        consulta.activa = False
        consulta.final = timezone.now()
        consulta.save()
        lectura = consulta.persona.lecturas_signos.last()
        emergencia = Emergencia()
        emergencia.persona = consulta.persona
        emergencia.historia_enfermedad_actual = consulta.HEA
        emergencia.usuario = consulta.consultorio.usuario
        if lectura is not None:
            emergencia.frecuencia_respiratoria = lectura.respiracion
            emergencia.temperatura = lectura.temperatura
            emergencia.presion = lectura.presion_arterial_media

        emergencia.tipo_de_venta = TipoVenta.objects.filter(
                predeterminada=True
        ).first()
        emergencia.save()

        messages.info(self.request, _('¡Se Envio el Paciente a Emergencias!'))
        return emergencia.get_absolute_url()


class NotaMedicaCreateView(ConsultaFormMixin, CurrentUserFormMixin, CreateView):
    """
    Creates a new :class:`NotaMedica`
    """
    model = NotaMedica
    form_class = NotaMedicaForm
