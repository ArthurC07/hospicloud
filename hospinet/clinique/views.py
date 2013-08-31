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

from django.views.generic import (TemplateView, DetailView, CreateView, View,
                                  ListView)
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin

from clinique.forms import (PacienteForm, CitaForm, EvaluacionForm,
                            ConsultaForm, SeguimientoForm, LecturaSignosForm)
from clinique.models import (Paciente, Cita, Consulta, Evaluacion,
                             Seguimiento, LecturaSignos)
from persona.views import PersonaFormMixin
from users.mixins import LoginRequiredMixin, CurrentUserFormMixin


class ConsultorioIndexView(ListView, LoginRequiredMixin):
    template_name = 'clinique/index.html'
    paginate_by = 20
    context_object_name = 'pacientes'

    def get_queryset(self):

        return Paciente.objects.filter(usuario=self.request.user).all()


class PacienteCreateView(CreateView, PersonaFormMixin, CurrentUserFormMixin,
                         LoginRequiredMixin):
    """Permite agregar una :class:`Persona` como un :class:`Paciente` de un
    doctor que tiene un :class:`User` en el sistema"""

    model = Paciente
    form_class = PacienteForm


class PacienteDetailView(DetailView, LoginRequiredMixin):
    """Permite ver los datos del :class"`Paciente` en la interfaz gráfica"""

    model = Paciente
    context_object_name = 'paciente'


class PacienteMixin(View):
    """Permite obtener un :class:`Paciente` desde los argumentos en una url"""

    def dispatch(self, *args, **kwargs):
        self.persona = get_object_or_404(Paciente, pk=kwargs['paciente'])
        return super(PacienteMixin, self).dispatch(*args, **kwargs)


class PacienteFormMixin(FormMixin, PacienteMixin):
    """Permite inicializar el paciente que se utilizará en un formulario"""

    def get_initial(self):
        initial = super(PacienteFormMixin, self).get_initial()
        initial = initial.copy()
        initial['persona'] = self.persona
        return initial


class CitaCreateView(PacienteFormMixin, CurrentUserFormMixin, CreateView,
                     LoginRequiredMixin):
    model = Cita
    form_class = CitaForm


class EvaluacionCreateView(PacienteFormMixin, LoginRequiredMixin, CreateView):
    model = Evaluacion
    form_class = EvaluacionForm


class ConsultaCreateView(PacienteFormMixin, CurrentUserFormMixin, CreateView,
                         LoginRequiredMixin):
    model = Consulta
    form_class = ConsultaForm


class SeguimientoCreateView(PacienteFormMixin, CurrentUserFormMixin, CreateView,
                            LoginRequiredMixin):
    model = Seguimiento
    form_class = SeguimientoForm


class LecturaSignosCreateView(PacienteFormMixin, LoginRequiredMixin, CreateView):
    model = LecturaSignos
    form_class = LecturaSignosForm
