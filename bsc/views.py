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

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    RedirectView, View
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from bsc.forms import RespuestaForm, VotoForm, VotoFormSet, QuejaForm, \
    ArchivoNotasForm, SolucionForm, RellamarForm
from bsc.models import ScoreCard, Encuesta, Respuesta, Voto, Queja, \
    ArchivoNotas, \
    Pregunta, Solucion, Login, Rellamar
from clinique.models import Consulta
from clinique.views import ConsultaFormMixin
from hospinet.utils.forms import PeriodoForm
from hospinet.utils.views import PeriodoView
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class ScoreCardListView(LoginRequiredMixin, ListView):
    model = ScoreCard

    def get_context_data(self, **kwargs):
        context = super(ScoreCardListView, self).get_context_data(**kwargs)

        context['loginperiodo'] = PeriodoForm(prefix='login')
        context['loginperiodo'].set_legend(
            _('Inicios de Sesi&oacute;n por Periodo')
        )
        context['loginperiodo'].set_action('login-periodo')

        return context


class ScoreCardDetailView(LoginRequiredMixin, DetailView):
    model = ScoreCard


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'bsc/user.html'


class EncuestaListView(LoginRequiredMixin, ListView):
    model = Encuesta


class EncuestaDetailView(LoginRequiredMixin, DetailView):
    model = Encuesta
    context_object_name = 'encuesta'
    queryset = Encuesta.objects.prefetch_related('respuesta_set')

    def get_context_data(self, **kwargs):
        context = super(EncuestaDetailView, self).get_context_data(**kwargs)

        context['consultas'] = self.object.consultas()

        return context


class EncuestaMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        return super(EncuestaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EncuestaMixin, self).get_context_data(**kwargs)

        context['encuesta'] = self.encuesta

        return context


class EncuestaFormMixin(EncuestaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(EncuestaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['encuesta'] = self.encuesta
        return initial


class RespuestaCreateView(EncuestaFormMixin, ConsultaFormMixin,
                          LoginRequiredMixin, CreateView):
    model = Respuesta
    form_class = RespuestaForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.persona = self.consulta.persona

        self.consulta.encuestada = True
        self.consulta.save()

        for pregunta in self.object.encuesta.pregunta_set.all():
            voto = Voto()
            voto.pregunta = pregunta
            voto.respuesta = self.object
            voto.save()

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class RespuestaDetailView(DetailView):
    model = Respuesta
    context_object_name = 'respuesta'
    queryset = Respuesta.objects.all().prefetch_related(
        'voto_set',
        'voto_set__opcion',
    )

    def get_context_data(self, **kwargs):
        context = super(RespuestaDetailView, self).get_context_data(**kwargs)

        formset = VotoFormSet(queryset=self.object.voto_set.all())
        for form in formset:
            form.fields[
                'opcion'].queryset = form.instance.pregunta.opcion_set.all()
            if not form.instance.pregunta.mostrar_sugerencia:
                form.fields['sugerencia'].widget = forms.HiddenInput()

        context['formset'] = formset
        context['helper'] = FormHelper()
        context['helper'].form_action = reverse('votos-guardar',
                                                args=[self.object.id])
        context['helper'].add_input(Submit('submit', _('Guardar')))

        context['queja'] = QuejaForm(initial={'respuesta': self.object})
        context['queja'].helper.form_id = 'queja'
        context['queja'].helper.form_action = reverse('queja-agregar',
                                                      args=[self.object.id])

        return context


def save_votes(request, respuesta):
    respuesta = get_object_or_404(Respuesta, pk=respuesta)
    if request.method == 'POST':
        formset = VotoFormSet(request.POST, respuesta.voto_set.all())
        if formset.is_valid():
            formset.save()
            respuesta.terminada = True
            respuesta.save()
        else:
            messages.info(request, _('La respuesta está incompleta'))
            return redirect(respuesta)
    else:
        messages.info(request, _('La respuesta está incompleta'))
        return redirect(respuesta)

    messages.info(request, _('Encuesta guardada!'))
    respuesta.consulta.encuestada = True
    respuesta.consulta.save()

    return redirect(respuesta.encuesta)


class RespuestaMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.respuesta = get_object_or_404(Respuesta, pk=kwargs['respuesta'])
        return super(RespuestaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RespuestaMixin, self).get_context_data(**kwargs)

        context['respuesta'] = self.respuesta

        return context


class RespuestaFormMixin(RespuestaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(RespuestaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['respuesta'] = self.respuesta
        return initial


class PreguntaMixin(ContextMixin, View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.pregunta = get_object_or_404(Pregunta, pk=kwargs['pregunta'])
        return super(PreguntaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreguntaMixin, self).get_context_data(**kwargs)

        context['pregunta'] = self.pregunta

        return context


class PreguntaFormMixin(PreguntaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(PreguntaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['pregunta'] = self.pregunta
        return initial


class VotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Voto
    form_class = VotoForm

    def get_form(self, form_class=None):
        form = super(VotoUpdateView, self).get_form(form_class)

        if self.object is not None:
            form.fields[
                'opcion'].queryset = self.object.pregunta.opcion_set.all()

        return form


class RespuestaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])

        respuesta = Respuesta()
        respuesta.consulta = consulta
        respuesta.encuesta = encuesta
        respuesta.persona = consulta.persona
        consulta.encuestada = True
        consulta.save()
        respuesta.save()

        for pregunta in encuesta.pregunta_set.all():
            voto = Voto()
            voto.pregunta = pregunta
            voto.respuesta = respuesta
            voto.save()

        return respuesta.get_absolute_url()


class ConsultaEncuestadaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])

        consulta.encuestada = True
        consulta.no_desea_encuesta = True
        consulta.save()

        return encuesta.get_absolute_url()


class ConsultaNoEncuestadaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        encuesta = get_object_or_404(Encuesta, pk=kwargs['encuesta'])
        consulta = get_object_or_404(Consulta, pk=kwargs['consulta'])

        consulta.encuestada = True
        consulta.save()

        return encuesta.get_absolute_url()


class QuejaCreateView(CreateView, RespuestaFormMixin, LoginRequiredMixin):
    model = Queja
    form_class = QuejaForm

    def get_success_url(self):
        return self.object.respuesta.get_absolute_url()


class QuejaDetailView(LoginRequiredMixin, DetailView):
    model = Queja
    queryset = Queja.objects.prefetch_related(
        'solucion_set',
    )


class QuejaListView(LoginRequiredMixin, ListView):
    model = Queja
    queryset = Queja.objects.filter(resuelta=False).select_related(
        'respuesta',
        'respuesta__persona',
        'respuesta__consulta',
        'respuesta__consulta__poliza',
        'respuesta__consulta__persona',
        'respuesta__consulta__poliza__aseguradora',
        'respuesta__consulta__consultorio__usuario',
    ).prefetch_related(
        'solucion_set',
        'respuesta__consulta__persona__contratos',
        'respuesta__consulta__poliza__contratos',
        'respuesta__consulta__persona__beneficiarios',
        'respuesta__consulta__persona__beneficiarios',
        'respuesta__consulta__persona__beneficiarios__contrato',
        'respuesta__consulta__persona__beneficiarios__contrato__persona',
        'respuesta__consulta__consultorio__secretaria',
        'respuesta__consulta__consultorio__usuario__profile',
        'respuesta__consulta__consultorio__usuario__profile__ciudad',
    )
    context_object_name = 'quejas'


class QuejaMixin(ContextMixin, View):
    def dispatch(self, *args, **kwargs):
        self.queja = get_object_or_404(Queja, pk=kwargs['queja'])
        return super(QuejaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuejaMixin, self).get_context_data(**kwargs)

        context['queja'] = self.queja

        return context


class QuejaFormMixin(QuejaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(QuejaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['queja'] = self.queja
        return initial


class SolucionCreateView(QuejaFormMixin, CurrentUserFormMixin, CreateView,
                         LoginRequiredMixin):
    model = Solucion
    form_class = SolucionForm


class ArchivoNotasCreateView(LoginRequiredMixin, CreateView):
    model = ArchivoNotas
    form_class = ArchivoNotasForm


class ArchivoNotasDetailView(LoginRequiredMixin, DetailView):
    model = ArchivoNotas
    context_object_name = 'archivonotas'


class ArchivoNotasProcesarView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        archivonotas = get_object_or_404(ArchivoNotas, pk=kwargs['pk'])
        archivonotas.procesar()

        messages.info(self.request, _('¡Archivo Importado Exitosamente!'))
        return archivonotas.get_absolute_url()


class LoginPeriodoView(PeriodoView, LoginRequiredMixin):
    prefix = 'login'
    redirect_on_invalid = 'scorecard-index'
    model = Login
    template_name = 'bsc/login_list.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPeriodoView, self).get_context_data(**kwargs)
        context['object_list'] = Login.objects.filter(
            created__range=(self.inicio, self.fin)
        ).order_by('user', 'created')

        return context


class RellamarCreateView(LoginRequiredMixin, EncuestaFormMixin,
                         ConsultaFormMixin, CreateView):
    model = Rellamar
    form_class = RellamarForm
