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
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    RedirectView

from django.views.generic.base import TemplateResponseMixin

from django.views.generic.edit import FormMixin

from bsc.forms import RespuestaForm, VotoForm, VotoFormSet
from bsc.models import ScoreCard, Encuesta, Respuesta, Voto
from clinique.models import Consulta
from clinique.views import ConsultaFormMixin
from users.mixins import LoginRequiredMixin


class ScoreCardListView(LoginRequiredMixin, ListView):
    model = ScoreCard


class ScoreCardDetailView(LoginRequiredMixin, DetailView):
    model = ScoreCard


class UserDetailView(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'bsc/user.html'


class EncuestaListView(LoginRequiredMixin, ListView):
    model = Encuesta


class EncuestaDetailView(LoginRequiredMixin, DetailView):
    model = Encuesta
    context_object_name = 'encuesta'

    def get_context_data(self, **kwargs):
        context = super(EncuestaDetailView, self).get_context_data(**kwargs)

        context['consultas'] = Consulta.objects.filter(facturada=True,
                                                       encuestada=False)

        return context


class EncuestaMixin(TemplateResponseMixin):
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

    def get_context_data(self, **kwargs):
        context = super(RespuestaDetailView, self).get_context_data(**kwargs)

        formset = VotoFormSet(queryset=self.object.voto_set.all())
        for form in formset:
            form.fields[
                'opcion'].queryset = form.instance.pregunta.opcion_set.all()

        context['formset'] = formset
        context['helper'] = FormHelper()
        context['helper'].form_action = reverse('votos-guardar',
                                                args=[self.object.id])
        context['helper'].add_input(Submit('submit', u'Guardar'))

        context['forms'] = []

        return context


def save_votes(request, respuesta):
    respuesta = get_object_or_404(Respuesta, pk=respuesta)
    if request.method == 'POST':
        formset = VotoFormSet(request.POST, respuesta.voto_set.all())
        if formset.is_valid():
            formset.save()
        else:
            messages.info(request, u'La respuesta está incompleta')
            return redirect(respuesta)
    else:
        messages.info(request, u'La respuesta está incompleta')
        return redirect(respuesta)

    messages.info(request, u'Encuesta guardada!')
    respuesta.consulta.encuestada = True
    respuesta.consulta.save()

    return redirect(respuesta.encuesta)


class RespuestaMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.respuesta = get_object_or_404(Encuesta, pk=kwargs['respuesta'])
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


class PreguntaMixin(TemplateResponseMixin):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.respuesta = get_object_or_404(Encuesta, pk=kwargs['respuesta'])
        return super(PreguntaMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreguntaMixin, self).get_context_data(**kwargs)

        context['encuesta'] = self.respuesta

        return context


class PreguntaFormMixin(PreguntaMixin, FormMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(PreguntaFormMixin, self).get_initial()
        initial = initial.copy()
        initial['respuesta'] = self.respuesta
        return initial


class VotoUpdateView(UpdateView, LoginRequiredMixin):
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
        consulta.encuestada = True
        consulta.save()
        respuesta.save()

        for pregunta in encuesta.pregunta_set.all():
            voto = Voto()
            voto.pregunta = pregunta
            voto.respuesta = respuesta
            voto.save()

        return respuesta.get_absolute_url()
