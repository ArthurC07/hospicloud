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

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (TemplateView, DetailView, CreateView,
                                  ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import RedirectView, View
from django.contrib import messages

from clinique.forms import (PacienteForm, CitaForm, EvaluacionForm)
from clinique.models import (Paciente, Cita, Consulta, Evaluacion)
from persona.forms import PersonaForm
from persona.models import Persona
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin, UserFormMixin

class ConsultorioIndexView(TemplateView):

    template_name = 'clinique/index.html'

class PacienteCreateView(CreateView, PersonaFormMixin, UserFormMixin,
                         LoginRequiredMixin):

    model = Paciente
    form_class = PacienteForm

class PacienteDetailView(DetailView, LoginRequiredMixin):

    model = Paciente
    context_object_name = 'paciente'

class PacienteMixin(SingleObjectMixin):

    model = Paciente
    pk_url_kwarg = 'paciente'

class PacienteFormMixin(PacienteMixin):

    def get_initial(self):
        initial = super(PacienteFormMixin, self).get_initial()
        initial = initial.copy()
        initial['persona'] = self.get_object()
        return initial


class CitaCreateView(PacienteFormMixin, UserFormMixin, CreateView,
                     LoginRequiredMixin):

    model = Cita
    form_class = CitaForm


class EvaluacionCreateView(PacienteFormMixin, CreateView, LoginRequiredMixin):
    model = Evaluacion
    form_class = EvaluacionForm
