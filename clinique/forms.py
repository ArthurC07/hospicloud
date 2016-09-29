# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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

from crispy_forms.layout import Fieldset, Submit
from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from clinique.models import Cita, Evaluacion, Seguimiento, Consulta, \
    LecturaSignos, Consultorio, DiagnosticoClinico, Cargo, OrdenMedica, \
    NotaEnfermeria, Examen, Espera, Prescripcion, Incapacidad, Reporte, \
    TipoConsulta, Remision, Afeccion, NotaMedica, OrdenLaboratorio, \
    OrdenLaboratorioItem
from contracts.models import MasterContract
from inventory.forms import ItemTemplateFormMixin
from inventory.models import ItemTemplate, ItemType
from persona.forms import FieldSetModelFormMixin, DateTimeWidget, \
    BasePersonaForm, FieldSetFormMixin
from persona.models import Persona
from users.mixins import HiddenUserForm
from django.contrib.auth.models import User


class ConsultorioFormMixin(FieldSetModelFormMixin):
    """
    Permite compartir agregar la información de consultorio automáticamente
    en los formularios que heredan de esta clase
    """
    consultorio = forms.ModelChoiceField(
        queryset=Consultorio.objects.select_related(
            'usuario',
        ).filter(activo=True).order_by(
            'nombre').all()
    )

class UserFormMixin(forms.Form):
    """
    Permite compartir agregar la información de usuarios automáticamente
    en los formularios que heredan de esta clase
    """
    medico = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__pk= 2)
    )  

class MedicoPeriodoForm(UserFormMixin):
    """
    Builds a form that allows specifying a :class:`Consultorio` and a
    Date range
    """
    
    inicio = forms.DateTimeField(widget=DateTimeWidget)
    fin = forms.DateTimeField(widget=DateTimeWidget)

    def __init__(self, *args, **kwargs):
        super(MedicoPeriodoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.field_names = self.fields.keys()
        self.helper.form_method = 'get'
        self.helper.layout = Fieldset(_('Consultas por Medico por Periodo'),
                                      *self.field_names)

    def set_action(self, action):
        self.helper.form_action = action

class HiddenConsultorioFormMixin(FieldSetModelFormMixin):
    consultorio = forms.ModelChoiceField(
        queryset=Consultorio.objects.select_related(
            'usuario',
        ).filter(activo=True).order_by(
            'nombre'
        ).all(),
        widget=forms.HiddenInput()
    )


class HiddenConsultaFormMixin(FieldSetModelFormMixin):
    consulta = forms.ModelChoiceField(
        queryset=Consulta.objects.all(),
        widget=forms.HiddenInput()
    )


class HiddenOrdenMedicaFormMixin(FieldSetModelFormMixin):
    orden = forms.ModelChoiceField(
        queryset=OrdenMedica.objects.all(),
        widget=forms.HiddenInput()
    )


class HiddenEsperaForm(FieldSetModelFormMixin):
    espera = forms.ModelChoiceField(
        queryset=Espera.objects.all(),
        widget=forms.HiddenInput()
    )


class ConsultaEsperaForm(HiddenConsultorioFormMixin, HiddenEsperaForm,
                         BasePersonaForm):
    """
    Creates a :class:`Consulta` using a :class:`Espera` data
    """

    class Meta:
        model = Consulta
        exclude = ('facturada', 'activa', 'final', 'remitida', 'encuestada',
                   'revisada', 'contrato', 'duracion', 'no_desea_encuesta')

    poliza = forms.ModelChoiceField(queryset=MasterContract.objects.all(),
                                    widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ConsultaEsperaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Consulta'), *self.field_names)


class ConsultaForm(HiddenConsultorioFormMixin, BasePersonaForm):
    """
    Builds a form that is used to create or edit :class:`Consulta`
    """

    class Meta:
        model = Consulta
        exclude = ('facturada', 'activa', 'final', 'remitida', 'encuestada',
                   'espera', 'revisada', 'contrato', 'duracion',
                   'no_desea_encuesta')

    tipo = forms.ModelChoiceField(
        queryset=TipoConsulta.objects.filter(habilitado=True).all())
    poliza = forms.ModelChoiceField(
        queryset=MasterContract.objects.select_related(
            'aseguradora',
            'plan',
            'contratante'
        ).filter(privado=True)
    )

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Consulta'), *self.field_names)


class EvaluacionForm(HiddenUserForm, BasePersonaForm, HiddenConsultaFormMixin):
    """
    Allows creating and editing :class:`Evaluacion` data
    """

    class Meta:
        model = Evaluacion
        fields = '__all__'

    cabeza = forms.ChoiceField(widget=forms.RadioSelect(),
                               choices=Evaluacion.NORMALIDAD)
    descripcion_cabeza = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )

    ojos = forms.ChoiceField(widget=forms.RadioSelect(),
                             choices=Evaluacion.NORMALIDAD)
    descripcion_ojos = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )

    cuello = forms.ChoiceField(widget=forms.RadioSelect(),
                               choices=Evaluacion.NORMALIDAD)
    descripcion_cuello = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )

    orl = forms.ChoiceField(widget=forms.RadioSelect(),
                            choices=Evaluacion.NORMALIDAD)
    descripcion_orl = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )
    gastrointestinal = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5,'class': 'form-control textarea'}), required=False
    )
    hallazgos_genitales = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )
    hallazgos_tacto_rectal = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )
    hallazgos_extremidades = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2,'class': 'form-control textarea'}), required=False
    )
    otras = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5,'class': 'form-control textarea'}), required=False
    )

    def __init__(self, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Evaluación'),
                                      *self.field_names)


class CitaForm(ConsultorioFormMixin):
    class Meta:
        model = Cita
        exclude = ('ausente', 'atendida',)

    persona = forms.ModelChoiceField(queryset=Persona.objects.all())
    fecha = forms.DateTimeField(widget=DateTimeWidget(), required=False,
                                initial=timezone.now)

    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar una Cita'), *self.field_names)


class CitaPersonaForm(CitaForm):
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )


class SeguimientoForm(BasePersonaForm, ConsultorioFormMixin, HiddenUserForm):
    class Meta:
        model = Seguimiento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SeguimientoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar una Segumiento'),
                                      *self.field_names)


class LecturaSignosForm(BasePersonaForm):
    class Meta:
        model = LecturaSignos
        exclude = ('presion_arterial_media',)

    def __init__(self, *args, **kwargs):
        super(LecturaSignosForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar una Lectura de Signos'),
                                      *self.field_names)


class DiagnosticoClinicoForm(BasePersonaForm, HiddenConsultaFormMixin,
                             HiddenUserForm):
    class Meta:
        model = DiagnosticoClinico
        fields = '__all__'

    afeccion = forms.ModelChoiceField(
        queryset=Afeccion.objects.all().order_by('nombre'),
        widget=autocomplete.ModelSelect2(url='afecciones'),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(DiagnosticoClinicoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar un Diagnóstico'),
                                      *self.field_names)


class ConsultorioForm(HiddenUserForm):
    class Meta:
        model = Consultorio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ConsultorioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Crear Consultorio'),
                                      *self.field_names)


class CargoForm(HiddenConsultaFormMixin, ItemTemplateFormMixin, HiddenUserForm):
    class Meta:
        model = Cargo
        exclude = ('facturado',)

    tipo = forms.ModelChoiceField(
        queryset=ItemType.objects.filter(consulta=True).all()
    )

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Cargo'), *self.field_names)


class OrdenMedicaForm(HiddenConsultaFormMixin, HiddenUserForm):
    class Meta:
        model = OrdenMedica
        exclude = ('facturada', 'farmacia')

    def __init__(self, *args, **kwargs):
        super(OrdenMedicaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Orden Médica'),
                                      *self.field_names)


class NotaEnfermeriaForm(BasePersonaForm, HiddenUserForm):
    class Meta:
        model = NotaEnfermeria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NotaEnfermeriaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Nota de Enfermeria'),
                                      *self.field_names)


class ExamenForm(BasePersonaForm):
    class Meta:
        model = Examen
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamenForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Examen'), *self.field_names)


class EsperaForm(BasePersonaForm, ConsultorioFormMixin, HiddenUserForm,
                 FieldSetModelFormMixin):
    class Meta:
        model = Espera
        fields = ('persona', 'consultorio', 'poliza', 'usuario')

    poliza = forms.ModelChoiceField(
        queryset=MasterContract.objects.select_related(
            'aseguradora',
            'plan',
            'contratante'
        ).filter(privado=True)
    )

    def __init__(self, *args, **kwargs):
        super(EsperaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Persona a la Sala de Espera'),
                                      *self.field_names)


class EsperaConsultorioForm(ConsultorioFormMixin, FieldSetModelFormMixin):
    class Meta:
        model = Espera
        fields = ('consultorio',)

    def __init__(self, *args, **kwargs):
        super(EsperaConsultorioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Cambiar Consultorio'),
                                      *self.field_names)


class EsperaAusenteForm(FieldSetModelFormMixin):
    class Meta:
        model = Espera
        fields = ('ausente',)

    def __init__(self, *args, **kwargs):
        super(EsperaAusenteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Marcar Espera como Ausente'),
                                      *self.field_names)


class CitaAusenteForm(FieldSetModelFormMixin):
    class Meta:
        model = Cita
        fields = ('ausente',)

    def __init__(self, *args, **kwargs):
        super(CitaAusenteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Marcar Cita como Ausente'),
                                      *self.field_names)


class PacienteSearchForm(FieldSetFormMixin):
    query = forms.CharField(label=_(u"Nombre o Identidad"))
    consultorio = forms.ModelChoiceField(queryset=Consultorio.objects.all())

    def __init__(self, *args, **kwargs):
        super(PacienteSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Buscar')))
        self.helper.layout = Fieldset(_('Buscar Paciente'), *self.field_names)
        self.helper.form_method = 'GET'
        self.helper.form_action = 'clinique-paciente-search'


class PrescripcionForm(HiddenOrdenMedicaFormMixin):
    class Meta:
        model = Prescripcion
        fields = '__all__'

    medicamento = forms.ModelChoiceField(
        queryset=ItemTemplate.objects.filter(activo=True).order_by(
            'descripcion'), required=False)

    def __init__(self, *args, **kwargs):
        super(PrescripcionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Prescripcion'),
                                      *self.field_names)


PrescripcionFormSet = inlineformset_factory(OrdenMedica, Prescripcion,
                                            PrescripcionForm)


class IncapacidadForm(BasePersonaForm, HiddenConsultaFormMixin, HiddenUserForm):
    class Meta:
        model = Incapacidad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncapacidadForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Incapacidad'),
                                      *self.field_names)


class ReporteForm(ConsultorioFormMixin):
    class Meta:
        model = Reporte
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Agregar Reporte'), *self.field_names)


class RemisionForm(ConsultorioFormMixin, BasePersonaForm):
    class Meta:
        model = Remision
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RemisionForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Remitir Paciente'), *self.field_names)


class NotaMedicaForm(HiddenConsultaFormMixin, HiddenUserForm):
    class Meta:
        model = NotaMedica
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NotaMedicaForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Nota Medica'),
                                      *self.field_names)


class OrdenLaboratorioForm(HiddenConsultaFormMixin):
    class Meta:
        model = OrdenLaboratorio
        exclude = ('enviado',)

    def __init__(self, *args, **kwargs):
        super(OrdenLaboratorioForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Orden de Laboratorio'),
                                      *self.field_names)


class OrdenLaboratorioItemForm(FieldSetModelFormMixin):
    """
    Builds a form that allows creating and editing :class:`OrdenLaboratorioItem`
    instances
    """
    class Meta:
        model = OrdenLaboratorioItem
        fields = '__all__'

    orden = forms.ModelChoiceField(queryset=OrdenLaboratorio.objects.all(),
                                   widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(OrdenLaboratorioItemForm, self).__init__(*args, **kwargs)
        self.helper.layout = Fieldset(_('Formulario de Orden de Laboratorio'),
                                      *self.field_names)

class AfeccionSearchForm(FieldSetFormMixin):
    query = forms.CharField(label=_("Nombre"))

    def __init__(self, *args, **kwargs):
        super(AfeccionSearchForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Buscar'))
        self.helper.layout = Fieldset(_('Buscar Afeccion'), *self.field_names)
        self.helper.form_method = 'GET'
        self.helper.form_action = 'afecciones-search'
