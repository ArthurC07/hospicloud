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

from crispy_forms.layout import Fieldset, Submit
from django import forms
from django.utils import timezone
from select2.fields import ModelChoiceField

from clinique.models import (Paciente, Cita, Evaluacion, Seguimiento,
                             Consulta, LecturaSignos, Consultorio,
                             DiagnosticoClinico, Cargo, OrdenMedica,
                             NotaEnfermeria, Examen, Espera, Prescripcion,
                             Incapacidad, Reporte, TipoConsulta, Remision)
from persona.forms import FieldSetModelFormMixin, DateTimeWidget, \
    BasePersonaForm, \
    FieldSetFormMixin
from persona.models import Persona
from users.mixins import HiddenUserForm
from inventory.models import ItemTemplate


class PacienteFormMixin(FieldSetModelFormMixin):
    paciente = forms.ModelChoiceField(label="", queryset=Paciente.objects.all(),
                                      widget=forms.HiddenInput(),
                                      required=False)


class PacienteForm(FieldSetModelFormMixin):
    """Permite editar los datos de un :class:`Paciente`"""

    class Meta:
        model = Paciente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Convertir en Paciente',
                                      *self.field_names)


class ConsultorioFormMixin(FieldSetModelFormMixin):
    consultorio = ModelChoiceField(
        queryset=Consultorio.objects.filter(activo=True).order_by(
            'nombre').all(),
        name="", model="", )


class HiddenConsultorioFormMixin(FieldSetModelFormMixin):
    consultorio = forms.ModelChoiceField(label="",
                                         queryset=Consultorio.objects.filter(
                                             activo=True).order_by(
                                             'nombre').all(),
                                         widget=forms.HiddenInput())


class ConsultaForm(PacienteFormMixin):
    class Meta:
        model = Consulta
        fields = '__all__'

    tipo = forms.ModelChoiceField(
        queryset=TipoConsulta.objects.filter(habilitado=True).all())

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Consulta', *self.field_names)


class EvaluacionForm(HiddenUserForm, PacienteFormMixin):
    class Meta:
        model = Evaluacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Evaluación',
                                      *self.field_names)


class CitaForm(ConsultorioFormMixin):
    class Meta:
        model = Cita
        exclude = ('ausente', 'atendida',)

    persona = ModelChoiceField(queryset=Persona.objects.all(), name="",
                               model="")
    fecha = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar una Cita', *self.field_names)


class CitaPersonaForm(CitaForm):
    persona = forms.ModelChoiceField(label="", queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput(), required=False)


class SeguimientoForm(PacienteFormMixin, HiddenUserForm):
    class Meta:
        model = Seguimiento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SeguimientoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar una Segumiento',
                                      *self.field_names)


class LecturaSignosForm(PacienteFormMixin):
    class Meta:
        model = LecturaSignos
        exclude = ('presion_arterial_media',)

    persona = forms.ModelChoiceField(label="", queryset=Persona.objects.all(),
                                     widget=forms.HiddenInput(), required=False)

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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ConsultorioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Crear Consultorio',
                                      *self.field_names)


class CargoForm(PacienteFormMixin):
    class Meta:
        model = Cargo
        fields = '__all__'

    item = ModelChoiceField(queryset=ItemTemplate.objects.all(), name="",
                            model="")

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Cargo', *self.field_names)


class OrdenMedicaForm(PacienteFormMixin):
    class Meta:
        model = OrdenMedica

    def __init__(self, *args, **kwargs):
        super(OrdenMedicaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Orden Médica',
                                      *self.field_names)


class NotaEnfermeriaForm(PacienteFormMixin, HiddenUserForm):
    class Meta:
        model = NotaEnfermeria

    def __init__(self, *args, **kwargs):
        super(NotaEnfermeriaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Nota de Enfermeria',
                                      *self.field_names)


class ExamenForm(PacienteFormMixin):
    class Meta:
        model = Examen

    def __init__(self, *args, **kwargs):
        super(ExamenForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Examen', *self.field_names)


class EsperaForm(BasePersonaForm, ConsultorioFormMixin, FieldSetModelFormMixin):
    class Meta:
        model = Espera

    fecha = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(EsperaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Persona a la Sala de Espera',
                                      *self.field_names)


class EsperaAusenteForm(FieldSetModelFormMixin):
    class Meta:
        model = Espera
        fields = ('ausente',)

    def __init__(self, *args, **kwargs):
        super(EsperaAusenteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Marcar Espera como Ausente',
                                      *self.field_names)


class CitaAusenteForm(FieldSetModelFormMixin):
    class Meta:
        model = Cita
        fields = ('ausente',)

    def __init__(self, *args, **kwargs):
        super(CitaAusenteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Marcar Cita como Ausente',
                                      *self.field_names)


class PacienteSearchForm(FieldSetFormMixin):
    query = forms.CharField(label=u"Nombre o Identidad")
    consultorio = forms.ModelChoiceField(queryset=Consultorio.objects.all())

    def __init__(self, *args, **kwargs):
        super(PacienteSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', u'Buscar'))
        self.helper.layout = Fieldset(u'Buscar Paciente', *self.field_names)
        self.helper.form_method = 'GET'
        self.helper.form_action = 'clinique-paciente-search'


class PrescripcionForm(PacienteFormMixin):
    class Meta:
        model = Prescripcion

    def __init__(self, *args, **kwargs):
        super(PrescripcionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Prescripcion',
                                      *self.field_names)


class IncapacidadForm(PacienteFormMixin, ConsultorioFormMixin):
    class Meta:
        model = Incapacidad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncapacidadForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Incapacidad', *self.field_names)


class ReporteForm(ConsultorioFormMixin):
    class Meta:
        model = Reporte
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Agregar Reporte', *self.field_names)


class RemisionForm(ConsultorioFormMixin, BasePersonaForm):
    class Meta:
        model = Remision
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RemisionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(u'Remitir Paciente', *self.field_names)
