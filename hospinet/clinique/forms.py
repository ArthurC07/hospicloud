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

from crispy_forms.layout import Fieldset
from django import forms
from django.contrib.auth.models import User

from clinique.models import (Paciente, Cita, Evaluacion, Seguimiento,
                             Consulta, LecturaSignos, Consultorio,
                             DiagnosticoClinico)
from persona.forms import FieldSetModelFormMixin
from users.mixins import HiddenUserForm, UserForm


class PacienteFormMixin(FieldSetModelFormMixin):
    paciente = forms.ModelChoiceField(label="", queryset=Paciente.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class PacienteForm(FieldSetModelFormMixin):
    """Permite editar los datos de un :class:`Paciente`"""

    class Meta:
        model = Paciente

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Convertir en Paciente',
                                      *self.field_names)


class ConsultaForm(PacienteFormMixin):
    class Meta:
        model = Consulta

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Consulta', *self.field_names)


class EvaluacionForm(HiddenUserForm, PacienteFormMixin):
    class Meta:
        model = Evaluacion

    def __init__(self, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Evaluación',
                                      *self.field_names)


class CitaForm(UserForm):
    class Meta:
        model = Cita

    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar una Cita', *self.field_names)


class SeguimientoForm(PacienteFormMixin, HiddenUserForm):
    class Meta:
        model = Seguimiento

    def __init__(self, *args, **kwargs):
        super(SeguimientoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar una Segumiento',
                                      *self.field_names)


class LecturaSignosForm(PacienteFormMixin):
    class Meta:
        model = LecturaSignos

    def __init__(self, *args, **kwargs):
        super(LecturaSignosForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar una Lectura de Signos',
                                      *self.field_names)

class DiagnosticoClinicoForm(PacienteFormMixin):
    class Meta:
        model = DiagnosticoClinico

    def __init__(self, *args, **kwargs):
        super(DiagnosticoClinicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar un Diagnóstico',
                                      *self.field_names)


class ConsultorioForm(HiddenUserForm):
    class Meta:
        model = Consultorio

    def __init__(self, *args, **kwargs):
        super(DiagnosticoClinicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Crear Consultorio',
                                      *self.field_names)
